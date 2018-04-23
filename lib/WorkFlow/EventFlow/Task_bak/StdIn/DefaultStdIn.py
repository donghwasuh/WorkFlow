import threading, time, select, json, requests

name = 'DefaultStdin'
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

class DefaultStdIn(threading.Thread):
    def __init__(self, task_manager, debugMode=False, recoveryMode=False):
        threading.Thread.__init__(self)
        self.task_manager = task_manager
        self.debugMode = debugMode
        self.recoveryMode = recoveryMode

        self.last_err_queue = []
        if self.debugMode: debugLog("init complete")

    def send_alert_data(self, data):
        if not self.task_manager.main_p.announcer_run: return
        url = '%s:%s%s' % ( self.task_manager.main_p.announcer_dst_addr, self.task_manager.main_p.announcer_dst_port, self.task_manager.main_p.announcer_alert_api )
        error_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        last_stdin, error_msg = data
        temp_dict = {}
        temp_dict['type'] = 'job'
        temp_dict['data'] = {}
        temp_dict['data']['jobName'] = self.task_manager.status['name']
        temp_dict['data']['datetime'] = error_time
        temp_dict['data']['message'] = ''.join(error_msg)
        temp_dict['data']['stdin'] = last_stdin
        json_data = json.dumps(temp_dict, indent=4)
        if not url.startswith('http'): url = 'http://' + url
        if self.debugMode:debugLog(url)
        if self.debugMode:debugLog(json_data)
        try:
            res = requests.post(url, headers={'Content-Type':'application/json'}, data=json_data)
            if self.debugMode:debugLog('alert data send result : %s' % str(res) )
        except Exception, e:
            if self.debugMode:debugLog('alert data send failed [%s]' % str(e))

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

    def put_stdin_manager(self, message):
        try:
            self.put_stdin(message)
            self.put_in_queue('stdin', message)
            if self.debugMode: debugLog( '[%s] in : %s' % ( self.task_manager.status['name'], repr(message) ) )
        except Exception, e:
            exceptionLog("Exception in put_stdin : %s" % str(e))

        while True:
            try: err_data, _, _ = select.select( [ self.task_manager.task_descriptor.stderr ], [], [], 1)
            except Exception, e: 
                err_data = ['']

            if len(err_data) > 0:
                err_msg = self.task_manager.task_descriptor.stderr.readline()
                if self.debugMode: debugLog( '[%s] err : %s' % (self.task_manager.status['name'], repr(err_msg)) )

                if err_msg == '':
                    err_message_index = 0
                    for line in self.last_err_queue:
                        if line.find('Exception') >= 0 or line.find('Traceback') >= 0: break
                        err_message_index += 1
                    if self.task_manager.status['status'] != 'TRM':
                        self.send_alert_data( (message, self.last_err_queue[err_message_index:]) )
                    self.last_err_queue = []
                    raise IOError, 'task killed'
                self.last_err_queue.append( err_msg )
                if len(self.last_err_queue) > 50:
                    self.last_err_queue = self.last_err_queue[len(self.last_err_queue) - 50:]
                self.put_in_queue('stderr', err_msg)
                
                if err_msg == '\n' or err_msg.strip() == str(message).strip():
                    if self.recoveryMode:
                        self.task_manager.status['status'] = 'TRM'
                        self.task_manager.shutdownFlag = True
                        self.task_manager.trm()
                        self.task_manager.main_p.thread_daemon_list['Core'].recovery_result[self.task_manager.recovery_name][1] = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    return err_msg
            else: pass
            if self.task_manager.shutdownFlag:
                raise IOError, 'task shutdown'

    def run(self):
        while self.task_manager.shutdownFlag == False:
            if self.task_manager.status['status'] == 'ACT':
                process_message_count = 0
                try:
                    for deq in self.task_manager.stdin_deq_list:
                        try:
                            msg = deq.popleft()
                            process_message_count += 1
                            self.put_stdin_manager(msg)
                            break
                        except Exception, e:
                            continue
                    if process_message_count == 0:
                        while self.task_manager.shutdownFlag == False:
                            try:
                                read_data, _, _, = select.select( [ self.task_manager.task_descriptor.stderr], [], [], 1 )
                            except Exception, e:
                                break
                            if len(read_data) > 0:
                                err_message = self.task_manager.task_descriptor.stderr.readline()
                                
                                # for manage error msg
                                self.last_err_queue.append( err_message  )
                                if len(self.last_err_queue) > 50:
                                    self.last_err_queue = self.last_err_queue[len(self.last_err_queue) - 50:]


                                if err_message == '':
                                    err_msg_index = 0
                                    for line in self.last_err_queue:
                                        if line.find('Exception') >= 0 or line.find('Traceback') >= 0: break
                                        err_msg_index += 1 
                                    if self.task_manager.status['status'] != 'TRM':
                                        self.send_alert_data( ('-', self.last_err_queue[err_msg_index:]) )
                                    ###### FIX ME : CALL ALARM RETURN 
                                    self.last_queue = []
                                    raise IOError, 'task killed'
                            
                                self.put_in_queue('stderr', err_message)
                                if self.debugMode: debugLog('[%s] stderr : %s' % ( self.task_manager.status['name'], repr(err_message)))
                            else: break
                except IOError, e:
                    if process_message_count != 0 and self.task_manager.main_p.error_data_file_skip == False:
                        deq.appendleft(msg)
                        if self.debugMode:debugLog("Excpetion in [%s] stdin thread : %s, message rollback" % ( self.task_manager.status['name'], str(e) ) )
                    else:
                        if self.debugMode:debugLog("Excpetion in [%s] stdin thread : %s, message drop" % ( self.task_manager.status['name'], str(e) ) )
                    time.sleep(1)
                except Exception, e:
                    if process_message_count != 0 and self.task_manager.main_p.error_data_file_skip == False:
                        deq.appendleft(msg)
                        if self.debugMode:debugLog("Excpetion in [%s] stdin thread : %s, message rollback" % ( self.task_manager.status['name'], str(e) ) )
                    else:
                        if self.debugMode:debugLog("Excpetion in [%s] stdin thread : %s, message drop" % ( self.task_manager.status['name'], str(e) ) )
                    time.sleep(1)
                finally:
                    if self.task_manager.shutdownFlag: break
            time.sleep(1)
