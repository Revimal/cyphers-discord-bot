import discord
import aiohttp
import asyncio
import json
from string import Formatter

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

class NeopleAPI:
    def __init__(self, subdir):
        with open('neople_api.token', 'r') as apikeyfile:
            self.apikey = apikeyfile.readline().strip()
        print('Neople APIKey is %s' % self.apikey)
        self.baseurl = 'https://api.neople.co.kr/cy/'
        self.subdir = subdir
        self.template = ""
        self.jsontoken = []
        self.prototype = {}

    def define_mdtemplate(self, filepath):
        with open(filepath, 'r') as fmtfile:
            self.template = fmtfile.read()
            self.jsontoken = [fn for _, fn, _, _ in Formatter().parse(self.template) if fn is not None]
            print('Jsontoken built %s' % self.jsontoken)

    def build_requrl(self, msg, optdir):
        if isinstance(msg, list):
            values = msg
        elif isinstance(msg, str):
            values = msg.split()
        else:
            values = str(msg).split()

        url = self.baseurl
        url += self.subdir
        if optdir is not None:
            url += '/'
            url += optdir
            url += '/'
        url += '?'

        for idx in range(min(len(values), len(self.prototype))):
            proto = self.prototype[idx]
            url += proto[0]
            url += '='
            if proto[1] is None:
                url += values[idx]
            else:
                url += proto[1]
            url += '&'

        url += 'apikey='
        url += self.apikey
        print('Request built %s' % url)
        return url

    async def req_apidata(self, msg, optdir=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.build_requrl(msg, optdir)) as response:
                if response.status != 200:
                    return None
                apidata = await response.text()
                print('Response data %s' % apidata)
                return apidata

    def access_jsondata(self, msg, rawtoken):
        try:
            jsonmsg = json.loads(msg)
            tokens = rawtoken.split('/')
            jsondata = None
            for token in tokens:
                if token.startswith('$'):
                    token = int(token[1:])
                if jsondata is None:
                    jsondata = jsonmsg[token]
                else:
                    jsondata = jsondata[token]
            return str(jsondata)
        except TypeError:
            return None
        except IndexError:
            return None

    def build_resmd(self, msg):
        parsed = {}
        for rawtoken in self.jsontoken:
            value = self.access_jsondata(msg, rawtoken)
            parsed[rawtoken] = value
        print('Parsed set %s' % str(parsed))
        return self.template.format(**parsed)

class CypUser(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players')
        self.prototype = {
                0 : ['nickname', None],
                1 : ['wordType', 'full'],
        }

class CypUserInfo(NeopleAPI, Singleton):
    def __init__(self):
        super().__init__('players')
        self.prototype = {}
        self.define_mdtemplate('user.md')

class CyphersBot(discord.Client, Singleton):
    async def on_ready(self):
        print('Logged on as', self.user )

    async def on_message(self, message):
        if message.author == self.user:
            return

        splited = message.content.split(' ')
        if splited[0] == '!user':
            response = '**Error Occurred**'
            raw_userid = await CypUser.instance().req_apidata(splited[1])
            if raw_userid is not None:
                userid = CypUser.instance().access_jsondata(raw_userid, 'rows/$0/playerId')
                raw_response = await CypUserInfo.instance().req_apidata(None, userid)
                if raw_response is not None:
                    response = CypUserInfo.instance().build_resmd(raw_response)
            await message.channel.send(response)

def main():
    with open('discord_bot.token', 'r') as botkeyfile:
        botkey = botkeyfile.readline().strip()
    print('Discord Botkey is %s' % botkey)
    CyphersBot.instance().run(botkey)

if __name__ == '__main__':
    main()
