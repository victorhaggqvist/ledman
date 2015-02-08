# coding=utf-8
from contextlib import contextmanager
import os
from bottle import request, abort, run, post, get, response, put
import daemon
import lockfile
import signal
from timeauth import TimeAuth
import control

__author__ = 'Victor Häggqvist'

auth = TimeAuth()
logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledman.log')
serverlog = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledman_daemon.log')
pidfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ledman.pid')


def log(msg):
    print('[server] '+msg)
    f = open(logfile, 'a+')
    f.write('[server] '+msg+"\n")
    f.close()

@get('/')
def home():
    return 'ledman is happy'

@post('/on')
def turn_on():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    log("turn on")
    control.turn_on()
    return ""


@post('/off')
def turn_off():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    log("turn off")
    control.turn_off()
    return ""


@put('/set/<color>')
def set_color(color=None):
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    level = request.query.level
    control.set_color(color, level)
    return ""


@get('/status')
def status():
    token = request.query.token
    timestamp = request.query.timestamp
    if not auth.auth(token, timestamp):
        abort(403)

    state = control.get_status()

    response.content_type = 'application/json: charset=utf8'
    return state


@contextmanager
def __locked_pidfile(filename):
    # Acquire the lockfile
    lock = lockfile.FileLock(filename)
    lock.acquire(-1)

    # Write out our pid
    realfile = open(filename, "w+")
    realfile.write(str(os.getpid()))
    realfile.close()

    # Yield to the daemon
    yield

    # Cleanup after ourselves
    os.remove(filename)
    lock.release()


def start_server(fork):
    """
    Start Bottle server
    :param fork: bool if we shall fork server
    :return:
    """
    if fork:
        f = open(serverlog, 'a+')

        context = daemon.DaemonContext(
            pidfile=__locked_pidfile(pidfile),
            stdout=f,
            stderr=f
            )
        log('starting server')
        log('forking to background')
        with context:
            run(host='127.0.0.1', port=8080)
    else:
        run(host='127.0.0.1', port=8080)
        # run(host='127.0.0.1', port=8080, debug=True)


def stop_server():
    if os.path.isfile(pidfile):
        log('stopping server..')
        with open(pidfile, "r") as p:
            pid = int(p.read())
            os.kill(pid, signal.SIGTERM)
            p.close()
        log('server stopped')
    else:
        log('server is down')


def status_server():
    if os.path.isfile(pidfile):
        f = open(pidfile, "r")
        pid = int(f.read())
        f.close()
        log('checking if pid '+str(pid)+' is running..')
        if check_pid(pid):
            log('server is running')
        else:
            log('server is down')
            os.remove(pidfile)
            log('removing old pidfile')
    else:
        log('server is down')


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
