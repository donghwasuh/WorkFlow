import threading, time, collections, os, sys, importlib, base64, json, shutil
import EventFlow.Task as Task

name = 'DefaultTask'
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

class DefaultTaskDelHelper:
    def __init__(self, main_process, name):
        self.main_p = main_process
        self.name = name

    #def _remove_work_directory(self):
    #    path = self.main_p.work_directory + '/' + self.name
    #    try:shutil.rmtree(path)
    #    except:pass

    #def _remove_dump_file(self):
    #    path = self.main_p.home_path + '/dmp/' + self.main_p.name + '/' + self.name
    #    try: os.remove(path + '_input.dmp')
    #    except:pass
    #    try: os.remove(path + '_output.dmp')
    #    except:pass

    def run(self):
        self._remove_work_directory()
        self._remove_dump_file()

class DefaultTaskHelper:
    def __init__(self, main_process, name, command, file_name, enc_data):
        self.main_p = main_process
        self.default_path = self._get_default_path()
        try: os.makedirs(self.default_path)
        except : pass
        self.name = name
        self.command = command
        self.file_name = file_name
        self.enc_data = enc_data
        if self.file_name:
            self.save_path = self.default_path + '/' + self.file_name
        else:
            self.save_path = None

    def _get_default_path(self):
        return self.main_p.home_path + '/data/' + self.main_p.name + '/bin'

    def _save_file(self):
        fd = open(self.save_path, 'w')
        fd.write(base64.decodestring(self.enc_data))
        fd.flush()
        fd.close()

    def _replace_command(self):
        pass

    def _do_specific(self):
        pass

    def _create_work_path(self):
        path = self.main_p.work_directory + '/' + self.name
        extract_path = path + '/extract'
        transform_path = path + '/transform'
        check_path = path + '/check'
        try: os.makedirs(extract_path)
        except: pass
        try: os.makedirs(transform_path)
        except: pass
        try: os.makedirs(check_path)
        except: pass

    def run(self):
        self._create_work_path()
        if self.file_name and self.enc_data:
            self._save_file()
            self._do_specific()
            command_string = self._replace_command()
        else:
            command_string = self.command
        return command_string

class DefaultTask(threading.Thread):
    def __init__(self, pname, command, main_process, debugMode=False, recoveryMode=False):
        threading.Thread.__init__(self)
        self.main_p = main_process
        self.debugMode = debugMode
        self.recoveryMode = recoveryMode
        self.shutdownFlag = False

        self.recovery_name = ''

        # make dmp folder and init path
        #self.dump_path = self.main_p.home_path + "/dmp/" + self.main_p.name
        #try: os.mkdir(self.dump_path)
        #except:pass
        #self.input_dump_path = self.dump_path + "/%s_input.dmp" % pname
        #self.output_dump_path = self.dump_path + "/%s_output.dmp" % pname

        # set first task descriptor with None
        self.task_descriptor = None

        # init status
        self.status = {}
        self.status['name'] = pname
        self.status['type'] = self.__class__.__name__.replace("Task", "").lower()
        self.status['command'] = command
        self.status['status'] = 'TRM'
        self.status['act-status'] = 'ABN'
        self.status['act-count'] = 1
        self.status['act-time'] = time.strftime("%Y%m%d%H%M%S", time.localtime( time.time() ) )
        self.status['last-status'] = {}
        self.status['last-status']['last-std-in'] = '-'
        self.status['last-status']['last-std-out'] = '-'
        self.status['last-status']['last-std-err'] = '-'

        # run process
        #self.task_run()

        # deque init for flow
        self.broadcast_deq = collections.deque()
        self.sharing_deq = collections.deque()
        self.broadcast_task_list = []
        self.sharing_task_list = []
        self.stdin_deq_list = [ self.broadcast_deq ]
        self.stdout_deq_list = []


        self.type_name = self.__class__.__name__.replace("Task", "").lower()

        try: self.task_stdin_thread_class = Task.default_stdin_setting[self.type_name]
        except: self.task_stdin_thread_class = None
        try: self.task_stdout_thread_class = Task.default_stdout_setting[self.type_name]
        except: self.task_stdout_thread_class = None


        self.task_stdin_thread = self.set_stdin_thread()
        self.task_stdout_thread = self.set_stdout_thread()


        if self.debugMode: debugLog("stdin thread class : %s" % self.task_stdin_thread_class)
        if self.debugMode: debugLog("stdout thread class : %s" % self.task_stdout_thread_class)

        self.out_deq = False


        self.sub_process_list = []

    def set_recovery_name(self, name):
        self.recovery_name = name

    def set_stdin_thread(self):
        if not self.task_stdin_thread_class: return None
        try:
            stdin_module = importlib.import_module(self.task_stdin_thread_class) 
            stdin_class = getattr(stdin_module, self.task_stdin_thread_class.split(".")[-1])(self, debugMode=self.debugMode, recoveryMode=self.recoveryMode)
            return stdin_class
        except Exception, e:
            exceptionLog("Exception in get stdin class : " + str(e))
        return None
        
    def set_stdout_thread(self):
        if not self.task_stdout_thread_class: return None
        try:
            stdout_module = importlib.import_module(self.task_stdout_thread_class) 
            stdout_class = getattr(stdout_module, self.task_stdout_thread_class.split(".")[-1])(self, debugMode=self.debugMode)
            return stdout_class
        except Exception, e:
            exceptionLog("Exception in get stdout class : " + str(e))
        return None

    def set_flow(self):
        self.stdin_deq_list = [ self.broadcast_deq ]
        self.stdout_deq_list = []

        for task in self.sharing_task_list:
            self.stdin_deq_list.append(task.sharing_deq)
        if self.out_deq:
            self.stdout_deq_list.append(self.sharing_deq)
        for task in self.broadcast_task_list:
            self.stdout_deq_list.append(task.broadcast_deq)

    def shutdown(self):
        self.shutdownFlag = True

    def clear_queue(self):
        evt_count = 0
        try:
            while True:
                self.broadcast_deq.pop()
                evt_count += 1
        except: pass
        try:
            while True:
                self.sharing_deq.pop()
                evt_count += 1
        except: pass
        return [ "OK : [%s] task's queue clear : %d events cleared\n" % ( self.status['name'], evt_count ) ]

    def put_queue(self, msg):
        if msg[-1] != '\n': msg + '\n'
        self.broadcast_deq.append(msg)

    def load_queue(self):
        return_message = []
        if self.recoveryMode: return [ 'OK : %s task run in recovery mode\n' % self.status['name'] ]
        if os.path.exists(self.input_dump_path):
            line_cnt = 0
            fd = open(self.input_dump_path, 'r')
            for line in fd:
                self.broadcast_deq.append(line)
                line_cnt += 1
            fd.close()
            return_message.append("OK : %s load %d input event from dump file\n" % (self.status['name'], line_cnt))
        else:
            return_message.append("NOK : %s input dump file not exists\n" % self.status['name'])
        if os.path.exists(self.output_dump_path):
            line_cnt = 0
            fd = open(self.output_dump_path, 'r')
            for line in fd:
                self.sharing_deq.append(line)
                line_cnt += 1
            fd.close()
            return_message.append("OK : %s load %d output event from dump file\n" % (self.status['name'], line_cnt))
        else:
            return_message.append("NOK : %s output dump file not exists\n" % self.status['name'])

        return return_message

    def save_queue(self):
        return_message = []
        if self.recoveryMode: return [ 'OK : %s task run in recovery mode\n' % self.status['name'] ]
        try:
            line_cnt = 0
            fd = open(self.input_dump_path, 'w')
            for line in self.broadcast_deq:
                fd.write(line)
                line_cnt += 1
            fd.flush()
            fd.close()
            return_message.append("OK : %s save %d input event to dump file\n" % (self.status['name'], line_cnt))
        except Exception, e:
            exceptionLog("Exception in save input event failed [ %s ]" % str(e))
            return_message.append("NOK : %s save input event failed [ %s ]\n" % (self.status['name'], str(e)))
        try:
            line_cnt = 0
            fd = open(self.output_dump_path, 'w')
            for line in self.sharing_deq:
                fd.write(line)
                line_cnt += 1
            fd.flush()
            fd.close()
            return_message.append("OK : %s save %d output event to dump file\n" % (self.status['name'], line_cnt))
        except Exception, e:
            exceptionLog("Exception in save input event failed [ %s ]" % str(e))
            return_message.append("NOK : %s save output event failed [ %s ]\n" % (self.status['name'], str(e)))

        return return_message

    def wait_close(self):
        self.join()

            

    def run(self):
        try:
            self.load_queue()
        except Exception, e:
            exceptionLog("Exception : " + str(e))

        self.set_flow()

        if self.task_stdin_thread: self.task_stdin_thread.start()
        if self.task_stdout_thread: self.task_stdout_thread.start()

        self.status['status'] = 'ACT'

        while self.shutdownFlag == False:
            if self.shutdownFlag: break
            if self.status['pid'] != '-' and self.status['status'] == 'ACT': 
                data = self.get_sub_process_list()
                if len(data) != 0: self.sub_process_list = data[:]
            
            if self.task_descriptor.poll() != None and self.status['status'] == 'ACT' and self.shutdownFlag == False:
                if self.debugMode:debugLog("terminate detected")
                self.status['act-status'] = 'ABN'
                if self.debugMode:debugLog("trm process")
                self.trm()
                if self.debugMode:debugLog("act process")
                self.act()
            else:
                self.status['act-status'] = 'OK'
            time.sleep(1)

        self.status['status'] = 'TRM'
        self.trm()
        
        try:
            self.save_queue()
        except Exception, e:
            exceptionLog("Exception : " + str(e))




if __name__ == '__main__':
    dt = DefaultTask('test', 'ls -alh', None)

