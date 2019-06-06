import aiohttp
import asyncio

class NeopleAPI:
    def __init__(self, subpath, tokenfile):
        self.baseurl = 'https://api.neople.co.kr/cy/'
        self.prototype = {}
        self.subpath = subpath
        with open(tokenfile, 'r') as apikeyfile:
            self.apikey = apikeyfile.readline().strip()
        print('Neople APIKey is %s' % self.apikey)

    def buildurl(self, msg, optpath):
        if msg is None:
            values = []
        elif isinstance(msg, list):
            values = msg
        elif isinstance(msg, str):
            values = msg.split()
        else:
            values = str(msg).split()

        url = self.baseurl
        url += self.subpath
        if optpath is not None:
            if not isinstance(optpath, list):
                optpath = [optpath]
            for opt in optpath:
                url += '/'
                url += opt
                url += '/'
        url += '?'

        for idx in range(len(self.prototype)):
            proto = self.prototype[idx]
            url += proto[0]
            url += '='
            if proto[1] is None:
                try:
                    url += values[idx]
                except IndexError:
                    pass
            else:
                url += str(proto[1])
            url += '&'

        url += 'apikey='
        url += self.apikey
        print('Request built %s' % url)
        return url

    async def request(self, msg, optpath=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.buildurl(msg, optpath)) as response:
                if response.status != 200:
                    return None
                apidata = await response.text()
                apidata = apidata.strip()
                print('Response data %s' % apidata)
                return apidata
