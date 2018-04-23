import threading, time


from EventFlow.Task.StdIn.DefaultStdIn import DefaultStdIn as DefaultStdIn

name = 'ProcessStdIn'
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

class ProcessStdIn(DefaultStdIn):
    def __init__(self, task_manager, debugMode=False, recoveryMode=False):
        DefaultStdIn.__init__(self, task_manager, debugMode=debugMode, recoveryMode=recoveryMode)

    def put_stdin(self, message):
        if message[-1] != '\n': message = message + '\n'
        try:
            self.task_manager.task_descriptor.stdin.write(message)
            self.task_manager.task_descriptor.stdin.flush()
        except Exception, e:
            normalLog("Exception in process stdin : %s" % str(e))
        
