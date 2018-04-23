import socket, threading, select, time, urllib2
from EventFlow.ThreadDaemon import ThreadDaemon
from EventFlow.MiddleInterface import MiddleInterface

name = 'WebMonitor'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

def exceptionLog(msg):
    __LOG__.Trace("E : %s : %s" % (name, msg))
    __LOG__.Exception()

class WebMonitor(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.web_listener = None

    def _web_listener_shutdown_request(self):
        self.web_listener.shutdownFlag = True
        url = 'http://127.0.0.1:%d%s' % (self.main_p.flask_port, self.main_p.flask_shutdown_code)
        try: r = urllib2.urlopen(url)
        except Exception, e:
            exceptionLog(str(e))

    def shutdown(self):
        self.shutdownFlag = True
        while True:
            self._web_listener_shutdown_request()
            if self.debugMode: debugLog('web listener shutdown called')
            if not self.web_listener.status: break
            time.sleep(1)

    def loop(self):
        self.web_listener = self.main_p.thread_daemon_list['WebListener']
        if not self.main_p.flask_run:
            if self.web_listener.status:
                self._web_listener_shutdown_request()

