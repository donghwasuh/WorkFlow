import threading, time

name = 'DefaultStdout'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
from EventFlow.Log import __LOG__
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

def exceptionLog(msg):
    __LOG__.Trace("E : %s : %s" % (name, msg))
    __LOG__.Exception()

class DefaultStdOut(threading.Thread):
    def __init__(self, task_manager, debugMode=False):
        threading.Thread.__init__(self)
        self.task_manager = task_manager
        self.debugMode = debugMode

    def put_in_queue(self, message_direction, message):
        try:
            if message_direction == 'stdin':
                message_direction = 'stdin  -> %s' % self.task_manager.status['name']
            elif message_direction == 'stdout':
                message_direction = '%s -> stdout' % self.task_manager.status['name']
            else:
                message_direction = '%s -> stderr' % self.task_manager.status['name']
            time_info = time.strftime( '%Y%m%d%H%M%S', time.localtime(time.time()) )
            self.task_manager.main_p.mon_deque.append( (time_info, message_direction, message) )
            self.task_manager.main_p.save_deque.append( (time_info, message_direction, message) )
        except Exception, e:
            exceptionLog( "Exception in put in deque : " + str(e) )

    def run(self):
        while self.task_manager.shutdownFlag == False:
            if self.task_manager.status['status'] == 'ACT':
                try:
                    msg = self.get_stdout()
                    self.put_in_queue('stdout', msg)
                    if self.debugMode: debugLog( '[%s] out : %s' % ( self.task_manager.status['name'], repr(msg) ) )

                    for deq in self.task_manager.stdout_deq_list:
                        while True:
                            if len(deq) < self.task_manager.main_p.max_cmd_queue_size:
                                deq.append(msg)
                                break
                            else:
                                if self.task_manager.shutdownFlag or self.task_manager.status['status'] == 'TRM':
                                    deq.append(msg)
                                    break
                                else:
                                    pass
                    if self.task_manager.shutdownFlag: break
                except IOError, e:
                    exceptionLog( "Exception in stdout run : " + str(e) )
                    time.sleep(1)
                except Exception, e:
                    exceptionLog( "Exception in stdout run : " + str(e) )
                    time.sleep(1)
                finally:
                    if self.task_manager.shutdownFlag: break
            else:
                time.sleep(1)
