# coding=utf-8
import logging
from time import time
import hashlib

__author__ = 'Victor Häggqvist'

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TimeAuth:
    timediff = 15  # minutes

    def __init__(self, keys):
        self.keys = keys

    def auth(self, token, timestamp):
        """
        Check function for timebased tokens

        token = sha256(apikey+timestamp)

        :param token: string Token hash
        :param timestamp: string
        :return: bool If authenticated
        """
        logger.debug('running')
        now = int(time())
        logger.debug('now  timestamp: '+str(now))
        logger.debug('hash timestamp: '+str(timestamp))

        mintime = now-(60*60*self.timediff)
        logger.debug('min  timestamp: '+str(mintime))
        if not self.check_tim(timestamp, mintime):
            return False

        logger.debug('time ok')
        for k in self.keys:
            logger.debug('test key: '+k)
            logger.debug(timestamp+k)
            tkn = (timestamp+k).encode('utf8')
            tkn2 = (k+timestamp).encode('utf8')
            logger.debug('gtoken: '+hashlib.sha256(tkn).hexdigest())
            logger.debug(' token: '+token)
            if token == hashlib.sha256(tkn).hexdigest():
                logger.debug('auth ok')
                return True
            elif token == hashlib.sha256(tkn2).hexdigest():
                logger.debug('auth ok')
                return True
            else:
                logger.debug('auth bad')
                return False

    @staticmethod
    def check_tim(hashtime, mintime):
        if int(hashtime) >= int(mintime):
            return True
        else:
            return False
