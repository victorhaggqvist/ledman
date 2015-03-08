#!/usr/bin/env python
# coding=utf-8
import argparse
import logging
from config import Config
config = Config()
import control
import server

__author__ = 'Victor Häggqvist'

# DEBUG = True
DEBUG = False

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('ledman')
fh = logging.FileHandler('ledman.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(fh)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help="Start command and control server", choices=['start', 'stop', 'status'])
    parser.add_argument('-n', '--on', help="Turn on lights", action='store_true')
    parser.add_argument('-f', '--off', help="Turn off lights", action='store_true')
    parser.add_argument('--nofork', help="Don't fork away server", action='store_true')
    parser.add_argument('-c', '--color', help="Color to set level for, used with --level", choices=['r', 'g', 'b'])
    parser.add_argument('-l', '--level', help="Set light level for color. Level is float 0.0 - 0.9 or 1, used with --color")
    args = parser.parse_args()

    if args.on:
        logger.info('turning lights on')
        control.turn_on()
    elif args.off:
        logger.info('turning lights off')
        control.turn_off()
    elif args.server == 'start' and args.nofork:
        logger.info('start server (no fork)')
        server.start_server(False)
    elif args.server == 'start':
        logger.info('start server')
        server.start_server(True)
    elif args.server == 'status':
        logger.info('server status')
        server.status_server()
    elif args.server == 'stop':
        logger.info('stop server')
        server.stop_server()
    elif args.color and args.level:
        logger.info('set color level')
        control.set_color(args.color, args.level)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
