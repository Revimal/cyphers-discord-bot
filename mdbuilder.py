from string import Formatter
import json

class MdBuilder:
    def __init__(self, filepath):
        with open(filepath, 'r') as fmtfile:
            self.template = fmtfile.read()
            self.jsontoken = [fn for _, fn, _, _ in Formatter().parse(self.template) if fn is not None]
        print('Jsontoken built %s' % self.jsontoken)

    def parse(self, msg, rawtoken, strtype=True):
        try:
            if isinstance(msg, str):
                jsonmsg = json.loads(msg)
            else:
                jsonmsg = msg
            tokens = rawtoken.split('/')
            jsondata = None
            for token in tokens:
                if token.startswith('$'):
                    token = int(token[1:])
                if jsondata is None:
                    jsondata = jsonmsg[token]
                else:
                    jsondata = jsondata[token]
            if strtype is True:
                jsondata = str(jsondata)
            return jsondata
        except TypeError:
            print('TypeError Occurred')
            return None
        except IndexError:
            print('IndexError Occurred')
            return None

    def build(self, msg, fmtstr=None):
        try:
            parsed = {}
            for rawtoken in self.jsontoken:
                value = self.parse(msg, rawtoken)
                parsed[rawtoken] = value
            print('Parsed set %s' % str(parsed))
            result = self.template.format(**parsed)
            if fmtstr is not None and isinstance(fmtstr, dict):
                for k, v in fmtstr.items():
                    result = result.replace('%' + k, str(v))
            return result
        except TypeError:
            return None
        except IndexError:
            return None
