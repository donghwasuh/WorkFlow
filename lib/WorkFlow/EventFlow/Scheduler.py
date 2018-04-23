import time
from EventFlow.ThreadDaemon import ThreadDaemon

name = 'Scheduler'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
Log.Init()

from EventFlow.Task.ProcessTask import ProcessTask as ProcessTask

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

def exceptionLog(msg):
    __LOG__.Trace("E : %s : %s" % (name, msg))
    __LOG__.Exception()



class Scheduler(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.before_time = None


    def _parsing_time(self, time_info, cron_format):
        timeStandard = []
        timeStandard.append(int(time_info[6:8]))
        timeStandard.append(int(time_info[4:6]))
        timeStandard.append(int(time_info[2:4]))
        timeStandard.append(int(time_info[:2]))
        timeStandard.append(int(time_info[8:]))

        cron = map(lambda x:x.strip(), cron_format.strip().split(" "))
        result = []
        for i in range(len(timeStandard)):
            if cron[i] == '*':
                result.append(True)
                continue
            if cron[i].find('/') >= 0:
                try:
                    value = int(cron[i].split("/")[-1].strip())
                    if timeStandard[i] % value == 0: result.append(True)
                    else: result.append(False)
                except:
                    result.append(False)
                continue
            if cron[1].find(",") >= 0:
                try:
                    value_list = map(lambda x:int(x), cron[i].split(","))
                    if timeStandard[i] in value_list: result.append(True)
                    else: result.append(False)
                except:
                    result.append(False)
                continue
            try:
                int_data = int(cron[i])
                if timeStandard[i] == int_data:
                    result.append(True)
                else:
                    result.append(False)
                continue
            except:
                result.append(False)
                continue

            result.append(False)
        if False in result: return False
        return True

    def loop(self):
        if not self.main_p.scheduler_run: return
        time_string = time.strftime("%m%d%H%M%w", time.localtime())
        time_string_for_send = time.strftime('%Y%m%d%H%M00', time.localtime())
        if not self.before_time:
            self.before_time = time_string
        if self.before_time == time_string:
            self.before_time = time_string
            return

        for schedule in self.main_p.schedule_conn.lst():
            if self._parsing_time(time_string, schedule[0]):
                if self.debugMode: debugLog('schedule started. [%s, %s, %s]' % schedule)
                message_default = schedule[2]
                if message_default.find('##DATE_TIME##') >= 0:
                    message_default = message_default.replace('##DATE_TIME##', time_string_for_send)
                try: self.main_p.thread_daemon_list['Core'].all_task_object[schedule[1]].put_queue(message_default)
                except Exception, e:
                    exceptionLog("%s schedule run failed [%s]" % ( str(schedule), str(e) ))
        self.before_time = time_string



                    

        
