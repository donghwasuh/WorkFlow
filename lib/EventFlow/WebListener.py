from flask import Flask, request, jsonify
from functools import wraps
import json, time

from EventFlow.ThreadDaemon import ThreadDaemon
from EventFlow.MiddleInterface import MiddleInterface
import EventFlow.MessageFormatter as MF
import EventFlow.WebListenerHelper as WLH

name = 'WebListener'
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

class WebListener(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.status = False
        self.app = Flask(__name__)
        self.middle_interface = MiddleInterface(self.main_p, web=True)
        self.api_version_prefix = '/api/v1/'
        self._init_web_listener()

    def _init_web_listener(self):

        def _call_error(message):
            error_msg = "NOK : %s" % message
            return MF.simple_result_json([error_msg])

        def pre_processing(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if self.debugMode:debugLog('decorator called by %s' % f.__name__)
                default_config = WLH._default_config.copy()
                try:
                    if f.__name__ not in default_config:raise Exception, '%s is not supported' % f.__name__

                    try: json_data = request.get_json()
                    except Exception, e: json_data = None

                    command = default_config[f.__name__](request.method, json_data, kwargs)
                    return self.middle_interface.command(command)
                except Exception, e:
                    exceptionLog(str(e))
                    error_msg = "NOK : Exception is occured in decorator [%s]" % str(e)
                    return MF.simple_result_json([error_msg])
            return decorated_function

        @self.app.route(self.api_version_prefix + 'configs', methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def configs(): pass

        @self.app.route(self.api_version_prefix + 'tasks', methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def tasks(): pass

        @self.app.route(self.api_version_prefix + 'schedules',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def schedules(): pass

        @self.app.route(self.api_version_prefix + 'flows',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def flows(): pass

        @self.app.route(self.api_version_prefix + 'groups',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def groups(): pass

        @self.app.route(self.api_version_prefix + 'tasks/<task_name>',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def task(task_name): pass

        @self.app.route(self.api_version_prefix + 'tasks/<task_name>/status',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def status(task_name): pass

        @self.app.route(self.api_version_prefix + 'tasks/<task_name>/queue',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def queue(task_name): pass

        @self.app.route(self.api_version_prefix + 'tasks/<task_name>/queue/stdin',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def stdin(task_name): pass

        @self.app.route(self.api_version_prefix + 'tasks/<task_name>/ready', methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def ready(task_name): pass

        @self.app.route(self.api_version_prefix + 'global_queue',  methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def global_queue(task_name): pass

        @self.app.route(self.api_version_prefix + 'recovery', methods = [ 'GET', 'POST', 'PUT', 'DELETE' ])
        @pre_processing
        def recovery(): pass
        

        def shutdown_func():
            func = request.environ.get('werkzeug.server.shutdown')
            if not func:
                normalLog('can not find flask shutdown function')
                return
            func()

        @self.app.route(self.main_p.flask_shutdown_code)
        def shutdown():
            shutdown_func()
            return 'flask shutting down'

       

    def loop(self):
        if self.debugMode: debugLog("flask run status : %s" % str(self.main_p.flask_run))
        while self.main_p.flask_run:
            self.status = True
            self.app.run(host='0.0.0.0', port=self.main_p.flask_port)
            self.status = False
            if self.shutdownFlag: break
        


