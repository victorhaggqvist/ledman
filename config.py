# coding=utf-8
from configparser import ConfigParser
import os

__author__ = 'Victor Häggqvist'


class Config:
    confdir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(confdir, 'ledman.conf')
    default = """
[gpio]
red=22
green=27
blue=17

[default_level]
red=0
green=0.3
blue=0.5

[server]
keys=testkeychangeme
    """

    def __init__(self):
        config = ConfigParser()

        if not os.path.isfile(self.config_file):
            self.init_config()

        config.read(self.config_file)

        self.GPIO_RED = config.get('gpio', 'red')  # 22
        self.GPIO_GREEN = config.get('gpio', 'green')  # 27
        self.GPIO_BLUE = config.get('gpio', 'blue')  # 17

        self.RED_DEFAULT = config.get('default_level', 'red')  # 0
        self.GREEN_DEFAULT = config.get('default_level', 'green')  # 0.3
        self.BLUE_DEFAULT = config.get('default_level', 'blue')  # 0.5

        keys = config.get('server', 'keys')

        self.keys = []
        for k in keys.split(','):
            self.keys.append(k)

    def init_config(self):
        f = open(self.config_file, 'w+')
        f.write(self.default)
        f.close()
