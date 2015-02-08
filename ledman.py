#!/usr/bin/env python
# coding=utf-8
import argparse
from config import Config
config = Config()
import control
import server

__author__ = 'Victor Häggqvist'

# DEBUG = True
DEBUG = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help="Start command and control server", choices=['start', 'stop', 'status'])
    parser.add_argument('-n', '--on', help="Turn on lights", action='store_true')
    parser.add_argument('-f', '--off', help="Turn off lights", action='store_true')
    parser.add_argument('--nofork', help="Don't fork away server", action='store_true')
    parser.add_argument('-c', '--color', help="Color to set level for, used with --level", choices=['r','g','b'])
    parser.add_argument('-l', '--level', help="Set light level for color. Level is float 0.0 - 0.9 or 1, used with --color")
    args = parser.parse_args()

    if args.on:
        print("[ledman] turning lights on")
        control.turn_on()
    elif args.off:
        print("[ledman] turning lights off")
        control.turn_off()
    elif args.server == 'start' and args.nofork:
        print("[ledman] start server (no fork)")
        server.start_server(False)
    elif args.server == 'start':
        print("[ledman] start server")
        server.start_server(True)
    elif args.server == 'status':
        print("[ledman] server status")
        server.status_server()
    elif args.server == 'stop':
        print("[ledman] stop server")
        server.stop_server()
    elif args.color and args.level:
        print("[ledman] set colorlevel")
        control.set_color(args.color, args.level)
        # print(args.color+'-c '+args.level+'-l')
    # elif args.set:
    #     print("setstuff")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
