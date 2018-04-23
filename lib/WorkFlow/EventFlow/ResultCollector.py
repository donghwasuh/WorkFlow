import time, psutil, subprocess, glob, os, json, requests
import EventFlow.Conf.Default as DefaultConfig
from EventFlow.ThreadDaemon import ThreadDaemon

name = 'ResultCollector'
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

class ResultCollector(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.before_time = None
        self.prev_system_cpu_jiffy = []
        self.value_list = {}
        self.result_data_dir = DefaultConfig.EVENTFLOW_HOME + '/log/' + self.main_p.name

    def send_result_data(self, data):
        if not self.main_p.announcer_run: return
        result_json_data = json.dumps(data, indent=4)
        url = '%s:%s%s' % ( self.main_p.announcer_dst_addr, self.main_p.announcer_dst_port, self.main_p.announcer_result_api )
        if not url.startswith('http'): url = 'http://' + url
        if self.debugMode:debugLog(url)
        if self.debugMode:debugLog(result_json_data)
        try:
            res = requests.post(url, headers={'Content-Type':'application/json'}, data=result_json_data)
            if self.debugMode:debugLog('result data send result : %s' % str(res) )
        except Exception, e:
            if self.debugMode:debugLog('result data send failed [%s]' % str(e))

    def _get_all_file_name(self, time_info):
        try:
            file_list = glob.glob(self.result_data_dir + '/*.log')
            del_time_info = time.strftime("%Y%m%d%H%M%S", time.localtime( time.time() - 3600 ))
            result_list = []
            del_list = []
            for _file in file_list:
                time_value = os.path.getmtime(_file)
                time_string = time.strftime('%Y%m%d%H%M%S', time.localtime(float(time_value)))
                if time_string >= time_info:
                    if self.debugMode: debugLog(time_info + "," + time_string)
                    result_list.append(_file)
                if time_string <= del_time_info:
                    del_list.append(_file)
        except Exception, e:
            exceptionLog('get all file name failed at %s [%s]' % (time_info, str(e)))
            result_list = []
        finally:
            for _file in del_list:
                try: os.remove(_file)
                except Exception, e: exceptionLog("remove log file [%s] failed. [%s]" % (_file, str(e)))
        return result_list

    def _line_time_checker(self, line, time_info, time_info_limit):
        try:
            time_data = line.strip().split(";")[0].strip()
            time_string = time.strftime("%Y%m%d%H%M%S", time.strptime(time_data, '%Y-%m-%d %H:%M:%S'))
            if time_info > time_string: return False
            if time_string >= time_info_limit: return False
        except Exception, e:
            return None
        return True

    def _get_all_line(self, file_list, time_info, time_info_limit):
        log_result = {}
        stat_result = {}
        
        for _file in file_list:
            process_name, file_type = os.path.basename(_file).rsplit("_", 1)[0].rsplit("_", 1)
            if file_type == 'LOG':
                if process_name not in log_result: log_result[process_name] = []
                temp_fd = open(_file, 'r')
                data = temp_fd.read()
                temp_fd.close()
                for line in data.split("\n"):
                    if len(line.strip()) == 0:continue
                    result = self._line_time_checker(line, time_info, time_info_limit)
                    if result == None:
                        if len(log_result[process_name]) == 0: continue
                        else: log_result[process_name][-1] = log_result[process_name][-1].strip() + ' ' + line.strip()
                    elif result:
                        log_result[process_name].append(line.strip())
        
            elif file_type == 'STATS':
                if process_name not in stat_result : stat_result[process_name] = []
                temp_fd = open(_file, 'r')
                data = temp_fd.read()
                temp_fd.close()
                for line in data.split("\n"):
                    if len(line.strip()) == 0:continue
                    result = self._line_time_checker(line, time_info, time_info_limit)
                    if result == None:
                        if len(stat_result[process_name]) == 0: continue
                        else: stat_result[process_name][-1] = stat_result[process_name][-1].strip() + ' ' + line.strip()
                    elif result:
                        stat_result[process_name].append(line.strip())
            else:
                continue
        
        del_key = []
        for _key in log_result:
            if len(log_result[_key]) == 0: del_key.append(_key)
        for _key in del_key:
            del log_result[_key]
        
        del_key = []
        for _key in stat_result:
            if len(stat_result[_key]) == 0: del_key.append(_key)
        for _key in del_key:
            del stat_result[_key]
        
        return { 'LOG' : log_result, 'STATS' : stat_result }

    def loop(self):
        time_string = time.strftime('%Y%m%d%H%M00', time.localtime())
        time_line = time.time()
        file_time_info = time.strftime('%Y%m%d%H%M00', time.localtime(time_line - 120))
        time_info = time.strftime('%Y%m%d%H%M00', time.localtime(time_line - 60))
        time_info_limit = time.strftime('%Y%m%d%H%M00', time.localtime(time_line))
        if not self.before_time:
            self.before_time = time_string
        if self.before_time == time_string:
            self.before_time = time_string
            return

        file_list = self._get_all_file_name(file_time_info)
        data = self._get_all_line(file_list, time_info, time_info_limit)
        self.send_result_data(data)
        self.before_time = time_string

