# coding=utf-8
from time import time
import hashlib
from ledman import config

__author__ = 'Victor Häggqvist'

def dprint(msg):
    if False:
        print('[auth] '+msg)

class TimeAuth:
    timediff = 15 # minutes
    def __init__(self):
        self.keys =  config.keys

    def auth(self, token, timestamp):
        """
        Check function for timebased tokens

        token = sha256(apikey+timestamp)

        :param token: string Token hash
        :param timestamp: string
        :return: bool If authenticated
        """
        dprint('running')
        now = int(time())
        dprint('now  timestamp: '+str(now))
        dprint('hash timestamp: '+str(timestamp))

        mintime = now-(60*60*self.timediff)
        dprint('min  timestamp: '+str(mintime))
        if not self.check_tim(timestamp, mintime):
            return False

        dprint('time ok')
        for k in self.keys:
            dprint('test key: '+k)
            dprint(timestamp+k)
            dprint('gtoken: '+hashlib.sha256(timestamp+k).hexdigest())
            dprint(' token: '+token)
            if token == hashlib.sha256(timestamp+k).hexdigest():
                return True
            elif token == hashlib.sha256(k+timestamp).hexdigest():
                return True
            else:
                return False

    def check_tim(self, hashtime, mintime):
        if hashtime >= mintime:
            return True
        else:
            return False
