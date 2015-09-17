# coding=utf-8
from contextlib import contextmanager
import logging
import os
from bottle import request, abort, run, post, get, response, put, Bottle
# import lockfile
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


# @contextmanager
# def __locked_pidfile(filename):
#     # Acquire the lockfile
#     lock = lockfile.FileLock(filename)
#     lock.acquire(-1)
#
#     # Write out our pid
#     with open(filename, "w+") as realfile:
#         realfile.write(str(os.getpid()))
#
#     # Yield to the daemon
#     yield
#
#     # Cleanup after ourselves
#     os.remove(filename)
#     lock.release()


# def start_server(fork):
#     """
#     Start Bottle server
#     :param fork: bool if we shall fork server
#     :return:
#     """
#     if fork:
#         with open(daemonlog, 'a+') as f:
#             context = daemon.DaemonContext(
#                 pidfile=__locked_pidfile(pidfile),
#                 stdout=f,
#                 stderr=f
#                 )
#             logger.info('starting server')
#             logger.info('forking to background')
#             with context:
#                 run(host='127.0.0.1', port=8080)
#
#     else:
#         fh = logging.FileHandler(serverlog)
#         fh.setLevel(logging.INFO)
#         fh.setFormatter(logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
#         logger.addHandler(fh)
#         run(host='127.0.0.1', port=8080, debug=True)


# def stop_server():
#     if os.path.isfile(pidfile):
#         logger.info('stopping server..')
#         with open(pidfile, "r") as p:
#             pid = int(p.read())
#             os.kill(pid, signal.SIGTERM)
#         logger.info('server stopped')
#     else:
#         logger.info('server is down')


def status_server():
    if os.path.isfile(pidfile):
        f = open(pidfile, "r")
        pid = int(f.read())
        f.close()
        logger.info('checking if pid '+str(pid)+' is running..')
        if check_pid(pid):
            logger.info('server is running')
        else:
            logger.info('server is down')
            os.remove(pidfile)
            logger.info('removing old pidfile')
    else:
        logger.info('server is down')


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
