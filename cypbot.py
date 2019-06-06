import discord
from neopleapi import NeopleAPI
from mdbuilder import MdBuilder

class Singleton:
    _instance = None
    
    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance

class CypUser(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players', 'neople_api.token')
        self.prototype = {
                0 : ['nickname', None],
                1 : ['wordType', 'full'],
        }

class CypUserInfo(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players', 'neople_api.token')

class CypRatingMatch(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players', 'neople_api.token')
        self.prototype = {
                0 : ['gameTypeId', 'rating'],
                1 : ['limit', 10]
        }
class CypRandomMatch(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players', 'neople_api.token')
        self.prototype = {
                0 : ['gameTypeId', 'normal'],
                1 : ['limit', 10]
        }
class UserInfoBuilder(MdBuilder, Singleton):
    def __init__(self):
        super().__init__('user.md')

class MatchListBuilder(MdBuilder, Singleton):
    def __init__(self):
        super().__init__('matchlist.md')

class CyphersBot(discord.Client, Singleton):
    def __init__(self):
        super().__init__()
        self.handlertbl = {
                'user' : self.handle_userinfo,
                'match' : self.handle_matchlist,
        }

    async def on_ready(self):
        print('Logged on as', self.user )

    async def on_message(self, message):
        if message.author == self.user:
            return

        splited = message.content.split(' ', 2)
        if splited[0] != '!cyp':
            return

        handler = self.handlertbl[splited[1]]
        if not callable(handler):
            return

        await message.channel.send(await handler(splited[2]))

    async def handle_userinfo(self, msg):
        rawdata = await CypUser.instance().request(msg)
        if rawdata is None:
            return '**API Error Occurred**'
        userid = UserInfoBuilder.instance().parse(rawdata, 'rows/$0/playerId')
        if userid is None:
            return '**User Not Found**'
        userdata = await CypUserInfo.instance().request(None, userid)
        if userdata is None:
            return '**API Error Occurred**'
        userinfo = UserInfoBuilder.instance().build(userdata)
        if userinfo is None:
            return '**Markdown Build Failed**'
        return userinfo

    async def handle_matchlist(self, msg):
        rawdata = await CypUser.instance().request(msg)
        if rawdata is None:
            return '**API Error Occurred**'
        userid = UserInfoBuilder.instance().parse(rawdata, 'rows/$0/playerId')
        if userid is None:
            return '**User Not Found**'
        userdata = await CypUserInfo.instance().request(None, userid)
        if userdata is None:
            return '**API Error Occurred**'
        ratingdata = await CypRatingMatch.instance().request(None, [userid, 'matches'])
        if ratingdata is None:
            return '**API Error Occurred**'
        randomdata = await CypRandomMatch.instance().request(None, [userid, 'matches'])
        if randomdata is None:
            return '**API Error Occurred**'

        fmtstr = {}
        ratingwin = 0
        ratinglose = 0
        ratinglist = MatchListBuilder.instance().parse(ratingdata, 'matches/rows', False);
        for i in range(10):
            try:
                matchres = MatchListBuilder.instance().parse(ratinglist[i], 'playInfo/result')
                if matchres == 'win':
                    ratingwin += 1
                    fmtstr['rating_' + str(i)] = '승'
                else:
                    ratinglose += 1
                    fmtstr['rating_' + str(i)] = '패'
            except IndexError:
                fmtstr['rating_' + str(i)] = 'X'
        randomwin = 0
        randomlose = 0
        randomlist = MatchListBuilder.instance().parse(randomdata, 'matches/rows', False) 
        for i in range(10):
            try:
                matchres = MatchListBuilder.instance().parse(randomlist[i], 'playInfo/result')
                if matchres == 'win':
                    randomwin += 1
                    fmtstr['random_' + str(i)] = '승'
                else:
                    randomlose += 1
                    fmtstr['random_' + str(i)] = '패'
            except IndexError:
                fmtstr['random_' + str(i)] = 'X'
        fmtstr['rating_win'] = ratingwin
        fmtstr['rating_lose'] = ratinglose
        fmtstr['random_win'] = randomwin
        fmtstr['random_lose'] = randomlose
        print('Fmtstr built %s' % fmtstr) 

        matchlist = MatchListBuilder.instance().build(userdata, fmtstr)
        if matchlist is None:
            return '**Markdown Build Failed**'
        return matchlist

def main():
    with open('discord_bot.token', 'r') as botkeyfile:
        botkey = botkeyfile.readline().strip()
    print('Discord Botkey is %s' % botkey)
    CyphersBot.instance().run(botkey)

if __name__ == '__main__':
    main()
