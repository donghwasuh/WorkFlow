import threading, time

from EventFlow.Task.StdOut.DefaultStdOut import DefaultStdOut

name = 'ProcessStdout'
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

class ProcessStdOut(DefaultStdOut):
    def __init__(self, task_manager, debugMode=True):
        DefaultStdOut.__init__(self, task_manager, debugMode=debugMode)

    def get_stdout(self):
        while True:
            try: stdout_read, _, _ = select.select( [ self.task_manager.task_descriptor.stdout ], [], [], 1)
            except: stdout_read = ['']

            if len(stdout_read) > 0:
                msg = self.task_manager.task_descriptor.stdout.readline()
                if msg == "":
                    raise IOError, 'process killed'
                else:
                    return msg

            else: pass
            if self.task_manager.shutdownFlag:
                raise IOError, 'process shutdown'
