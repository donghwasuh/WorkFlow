import threading, time

name = 'ThreadDaemon'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))


# Thread Daemon is all thread daemon's base
class ThreadDaemon(threading.Thread):
    def __init__(self, main_process, debugMode=True):
        threading.Thread.__init__(self)
        # get Main Processor
        self.main_p = main_process
        self.debugMode = debugMode
        self.shutdownFlag = False
        self.firstRun = False

    # shutdown flag manage
    def shutdown(self):
        if self.debugMode: debugLog("%s daemon shutdown called" % self.__class__.__name__)
        self.shutdownFlag = True
        normalLog("%s daemon shutdown flag setted" % self.__class__.__name__)

    # do call() function every 1 sec
    def run(self):
        self.firstRun = True
        if self.debugMode: debugLog("%s daemon started" % self.__class__.__name__)
        while True:
            if self.debugMode:debugLog('%s daemon is running' % self.__class__.__name__)
            if self.shutdownFlag:
                if self.debugMode: debugLog("%s daemon shutdown now" % self.__class__.__name__)
                break 
            self.loop()
            time.sleep(1)
