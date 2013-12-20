import urllib
import hashlib

class LingrBot:

    def __init__(self, room, name, secret):
        self.room = room
        self.name = name
        self.secret = secret

    def gen_verifier(self):
        sha1 = hashlib.sha1(self.name + self.secret)
        return sha1.hexdigest()

    def gen_params(self, say):
        params = {
            'room': self.room,
            'bot': self.name,
            'text': say,
            'bot_verifier': self.gen_verifier()}
        urlparams = urllib.urlencode(params)
        return urlparams

    def do_post(self, say):
        params = self.gen_params(say)
        response = urllib.urlopen(
            'http://lingr.com/api/room/say', params)
