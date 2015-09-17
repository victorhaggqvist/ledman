# coding=utf-8
import logging
import os
from ledman import config
import json

DEBUG = False

__author__ = 'Victor Häggqvist'

logger = logging.getLogger(__name__)
statefile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledstate.json')


def store_state(pin, brightness):
    try:
        with open(statefile, "r") as store:
            state = store.read()
            statejson = json.loads(state)
    except:
        statejson = {}

    statejson[get_color_by_pin(pin)] = brightness
    ujson = json.dumps(statejson)

    with open(statefile,'w') as store:
        store.write(ujson)


def set_gpio(pin, brightness):
    if DEBUG:
        logger.info('not actually doing echo '+pin+'='+brightness+' > /dev/pi-blaster')
        store_state(pin, brightness)
    else:
        os.system('echo "'+pin+'='+brightness+'" > /dev/pi-blaster')
        store_state(pin, brightness)
        logger.info('set pin '+pin+' at level '+brightness)


def turn_on():
    set_gpio(config.GPIO_RED, config.RED_DEFAULT)
    set_gpio(config.GPIO_GREEN, config.GREEN_DEFAULT)
    set_gpio(config.GPIO_BLUE, config.BLUE_DEFAULT)


def turn_off():
    set_gpio(config.GPIO_RED, '0')
    set_gpio(config.GPIO_GREEN, '0')
    set_gpio(config.GPIO_BLUE, '0')


def get_pin_by_color(color):
    return {
        "r": config.GPIO_RED,
        "g": config.GPIO_GREEN,
        "b": config.GPIO_BLUE
    }[color]


def get_color_by_pin(pin):
    return {
        config.GPIO_RED: 'r',
        config.GPIO_GREEN: 'g',
        config.GPIO_BLUE: 'b'
    }[pin]


def set_color(color, level):
    """
    Set color pin to level
    :param color: str
    :param level: str
    :return:
    """
    ok = True
    if color not in ['r', 'g', 'b']:
        ok = False

    if len(level) > 3:
        ok = False

    if level in ['0', '1']:
        ok = True

    if len(level) == 3 and is_float(level) and float(level) < 1:
        ok = True

    if ok:
        logger.info('set color '+color+' at level '+level)
        pin = get_pin_by_color(color)
        set_gpio(pin, level)
        return False
    else:
        logger.info('set color, unrecognized combination: color '+color+' at level '+level)
        return False


def get_status():
    f = open(statefile, 'r')
    state = f.read()
    f.close()
    return state


def is_float(num_string):
    try:
        float(num_string)
        return True
    except:
        return False
