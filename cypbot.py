import hashlib
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
                'help' : [self.handle_helpcmd,
                    '`!cyp help` 디스코드 봇 사용법을 출력합니다'],
                'issue' : [self.handle_issue,
                    '`!cyp issue {Message}` 사용중 발견한 버그나 개선사항을 140자 이하로 적어주세요'],
                'user' : [self.handle_userinfo,
                    '`!cyp user {Username}` 입력한 유저의 기본 정보를 가져옵니다'],
                'match' : [self.handle_matchlist,
                    '`!cyp match {Username}` 입력한 유저의 최근 전적을 가져옵니다']
        }
        with open('report_channel.token', 'r') as reportidfile:
            self.reportchanid = int(reportidfile.readline().strip())
        print('Report Channel ID is %s' % str(self.reportchanid))
        with open('notify_md5.token', 'r') as notikeyfile:
            self.notifykey = notikeyfile.readline().strip()
        print('Notify Password is %s' % self.notifykey)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        splited = message.content.split(' ', 2)
        
        if splited[0] == '!cyp-admin-notify':
            try:
                notipw = splited[1]
                notimsg = splited[2]
                hasher = hashlib.md5(notipw.strip().encode('utf-8'))
                if hasher.hexdigest() == self.notifykey:
                    print('Notify sent %s' % notimsg)
                    await self.send_notify(notimsg)
                else:
                    print('Someone tried to send notify %s / %s' % (notipw, notimsg))
                return
            except IndexError:
                return
        elif splited[0] != '!cyp':
            return

        try:
            command = splited[1]
        except IndexError:
            command = 'help'
        try:
            cmdargs = splited[2]
        except IndexError:
            cmdargs = None

        try:
            handler = self.handlertbl[command]
        except KeyError:
            return

        if not callable(handler[0]):
            return

        await message.channel.send(await handler[0](cmdargs))

    async def send_notify(self, msg):
        for channel in self.get_all_channels():
            try:
                await channel.send(msg)
            except:
                pass

    async def handle_helpcmd(self, msg):
        helpmsg = '**[도움말]**'
        for cmdidx in list(self.handlertbl.values()):
            helpmsg += '\n'
            helpmsg += cmdidx[1]
        return helpmsg

    async def handle_issue(self, msg):
        try:
            limitlen = min(len(msg), 140)  
            limitmsg = '```' + msg[0:limitlen] + '```'
            await self.get_channel(self.reprtchanid).send(limitmsg)
            print('Someone reported an issue')
        except AttributeError:
            print('Invalid report channel')
        except IndexError:
            print('Index Error Occurred')
        return '**Thank you for reporting the issue**'

    async def handle_userinfo(self, msg):
        rawdata = await CypUser.instance().request(msg)
        if rawdata is None:
            return '**Invalid Command, `!cyp help` always be with you!**'
        userid = UserInfoBuilder.instance().parse(rawdata, 'rows/$0/playerId')
        if userid is None:
            return '**User Not Found**'
        userdata = await CypUserInfo.instance().request(None, userid)
        if userdata is None:
            return '**API Error Occurred**'
        
        rating_idx = None
        random_idx = None

        if UserInfoBuilder.instance().parse(userdata, 'records/$0/gameTypeId') == 'rating':
            rating_idx = '$0'
        elif UserInfoBuilder.instance().parse(userdata, 'records/$1/gameTypeId') == 'rating':
            rating_idx = '$1'

        if UserInfoBuilder.instance().parse(userdata, 'records/$0/gameTypeId') == 'normal':
            random_idx = '$0'
        elif UserInfoBuilder.instance().parse(userdata, 'records/$1/gameTypeId') == 'normal':
            random_idx = '$1'

        if rating_idx is not None:
            rating_win = UserInfoBuilder.instance().parse(userdata, 'records/' + rating_idx + '/winCount', False)
            rating_lose = UserInfoBuilder.instance().parse(userdata, 'records/'+ rating_idx + '/loseCount', False)
            rating_stop = UserInfoBuilder.instance().parse(userdata, 'records/' + rating_idx + '/stopCount', False)
            try:
                rating_winrate = round(float(rating_win) / float(rating_win + rating_lose + rating_stop) * 100.0, 2)
            except ZeroDivisionError:
                rating_winrate = None
        else:
            rating_win = None
            rating_lose = None
            rating_stop = None
            rating_winrate = None

        if random_idx is not None:
            random_win = UserInfoBuilder.instance().parse(userdata, 'records/' + random_idx + '/winCount', False)
            random_lose = UserInfoBuilder.instance().parse(userdata, 'records/' + random_idx + '/loseCount', False)
            random_stop = UserInfoBuilder.instance().parse(userdata, 'records/' + random_idx + '/stopCount', False)
            try:
                random_winrate = round(float(random_win) / float(random_win + random_lose + random_stop) * 100.0, 2)
            except ZeroDivisionError:
                random_winrate = None
        else:
            random_win = None
            random_lose = None
            random_stop = None
            random_winrate = None
        
        fmtstr = {}
        fmtstr['rating_wincount'] = str(rating_win)
        fmtstr['rating_losecount'] = str(rating_lose)
        fmtstr['rating_stopcount'] = str(rating_stop)
        fmtstr['rating_winrate'] = str(rating_winrate)
        fmtstr['random_wincount'] = str(random_win)
        fmtstr['random_losecount'] = str(random_lose)
        fmtstr['random_stopcount'] = str(random_stop)
        fmtstr['random_winrate'] = str(random_winrate)

        userinfo = UserInfoBuilder.instance().build(userdata, fmtstr)
        if userinfo is None:
            return '**Markdown Build Failed**'
        return userinfo

    async def handle_matchlist(self, msg):
        rawdata = await CypUser.instance().request(msg)
        if rawdata is None:
            return '**Invalid Command, `!cyp help` always be with you!**'
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
