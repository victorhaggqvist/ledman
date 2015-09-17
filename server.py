# coding=utf-8
import logging
import os
from bottle import request, abort, run, response, Bottle
from timeauth import TimeAuth
from ledman import config
import control

__author__ = 'Victor Häggqvist'

app = application = Bottle()

auth = TimeAuth(config.keys)

logger = logging.getLogger(__name__)
daemonlog = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledman_daemon.log')
serverlog = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server.log')
pidfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledman.pid')


@app.get('/')
def home():
    return 'ledman is happy'


@app.post('/on')
def turn_on():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    ip = request.environ.get('REMOTE_ADDR')
    logger.info('client %s: turn on', ip)
    control.turn_on()
    return ""


@app.post('/off')
def turn_off():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    ip = request.environ.get('REMOTE_ADDR')
    logger.info('client %s: turn off', ip)
    control.turn_off()
    return ""


@app.put('/set/<color>')
def set_color(color=None):
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    level = request.query.level
    ip = request.environ.get('REMOTE_ADDR')
    logger.info('client %s: set color %s at %s', ip, color, level)
    control.set_color(color, level)
    return ""


@app.get('/status')
def status():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    ip = request.environ.get('REMOTE_ADDR')
    logger.info('client %s: status request', ip)
    state = control.get_status()

    response.content_type = 'application/json: charset=utf8'
    return state

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    try:
        import python_server
        run(app=StripPathMiddleware(app),
            server='python_server',
            host='0.0.0.0',
            port=8080)
    except:
        run(app=app)
