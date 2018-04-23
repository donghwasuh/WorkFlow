import threading, time, collections, subprocess, sys, os, psutil


import EventFlow.Task as Task

from EventFlow.Task.DefaultTask import DefaultTask as DefaultTask
from EventFlow.Task.DefaultTask import DefaultTaskHelper as DefaultTaskHelper
from EventFlow.Task.DefaultTask import DefaultTaskDelHelper as DefaultTaskDelHelper


name = 'ProcessTask'
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

class ProcessTaskDelHelper(DefaultTaskDelHelper):
    def __init__(self, main_p, name):
        DefaultTaskDelHelper.__init__(self, main_p, name)

class ProcessTaskHelper(DefaultTaskHelper):
    def __init__(self, main_process, name, command, file_name, enc_data):
        DefaultTaskHelper.__init__(self,main_process, name, command, file_name, enc_data)

    def _replace_command(self):
        return self.command.replace(self.file_name, self.save_path)

class ProcessTask(DefaultTask):
    def __init__(self, pname, command, main_process, debugMode=False, recoveryMode=False):
        DefaultTask.__init__(self, pname, command, main_process, debugMode=debugMode, recoveryMode=recoveryMode)

    def task_run(self):
        try:
            my_env = os.environ
            self.task_descriptor = subprocess.Popen( self.status['command'], shell=True, bufsize=0,
                                                        stdin=subprocess.PIPE,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE, close_fds=True, env=my_env )
            self.status['pid'] = self.task_descriptor.pid
            self.status['status'] = 'ACT'
        except Exception,e:
            while True:
                try:
                    if self.task_descriptor.poll() == None:
                        self.task_descriptor.terminate()
                        sys.stderr.write("ProcessTask : %s task run term itself\n" % self.status['name'])
                        time.sleep(1)
                        self.task_descriptor.kill()
                        sys.stderr.write("ProcessTask : %s task run kill itself\n" % self.status['name'])
                        if self.shutdownFlag or self.stat == 'TRM' : break
                    else: break
                except: break
            sys.stderr.write("ProcessTask : %s task run failed\n" % self.status['name'])
            exceptionLog("%s task run failed [%s]\n" % (self.status['name'], str(e)))

    def act(self):
        if self.task_descriptor.poll() == None:
            return [ "NOK : %s [ %s ] already alive\n" % (self.status['name'], self.status['command'][:10]) ]
        else:
            self.status['act-count'] += 1
            self.task_run()
            self.status['act-time'] = time.strftime("%Y%m%d%H%M%S", time.localtime( time.time() ) )
            return [ "OK : %s [ %s ] started\n" % (self.status['name'], self.status['command'][:10]) ]

    def trm(self):
        ret_list = []
        self.status['status'] = 'TRM'
        self.status['act-status'] = 'ABN'
        try:  
            parent = psutil.Process(self.status['pid'])
            sub_process = parent.children(recursive=True)
        except Exception, e:
            exceptionLog("Exception in trm, get sub process : %s" % str(e))
            sub_process = self.sub_process_list[:]

        try:
            self.task_descriptor.terminate()
            normalLog("call terminate signal for [%s] task" % self.status['name'])
            
            if self.task_descriptor.poll() == None:
                kill_status = False
                while True:
                    for sec in range(self.main_p.kill_wait_time):
                        if self.task_descriptor.poll() != None: 
                            kill_status = True
                            break
                        time.sleep(1)
                    if kill_status: break
                    normalLog("[%s] task still alive" % self.status['name'])
                    self.task_descriptor.kill()
                    normalLog("call kill signal for [%s] task" % self.status['name'])
            normalLog("[%s] task is killed" % self.status['name'])
            retry_count = 0
            while True:
                if len(sub_process) == 0: break
                check_list = []
                for child in sub_process:
                    try:
                        if child.is_running():
                            if child.parent() == None or child.parent().pid == 1 or child.parent().pid == self.status['pid']:
                                if retry_count <= 3 :
                                    child.terminate()
                                    check_list.append(child)
                                    normalLog("call term signal for [%s] task's child [%d]" % ( self.status['name'], child.pid ))
                                else:
                                    child.kill()
                                    check_list.append(child)
                                    normalLog("call kill signal for [%s] task's child [%d]" % ( self.status['name'], child.pid ))
                    except psutil.NoSuchProcess: continue
                    except Exception, e:
                        exceptionLog("Exception in trm, term [%s] task's child [%d]" % ( self.status['name'], child.pid ))
                sub_process = check_list[:]
                retry_count += 1
        except Exception, e:
            return ['NOK : trm [%s] task failed with exception : %s\n' % ( self.status['name'], str(e) )]

        self.status['pid'] = '-'
        self.status['status'] = 'TRM'
        self.status['act-status'] = 'OK'
        self.status['act-count'] = 0

        return ['OK : %s [ %s ] killed\n' % (self.status['name'], self.status['command'][:10]) ]

    def get_sub_process_list(self):
        try:  
            parent = psutil.Process(self.status['pid'])
            sub_process = parent.children(recursive=True)
        except Exception, e:
            exceptionLog("Exception in trm, get sub process : %s" % str(e))
            sub_process = []
        return sub_process
       

class dummyMainProcess:
    def __init__(self):
        self.home_path = "/home/wckang85/EventFlow/EventFlowSingle"
        self.name = "test"
        self.max_cmd_queue_size = 10


if __name__ == '__main__':
    dm = dummyMainProcess()
    pt = ProcessTask( 'test', 'python /home/wckang85/EventFlow/EventFlowSingle/testProgram/test_program_in_out.py test', dm, debugMode=True)
    pt.start()
    while True:
        pt.put_queue("test\n")
        time.sleep(1)
            
