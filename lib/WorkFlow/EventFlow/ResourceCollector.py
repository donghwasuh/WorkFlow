import time, psutil, subprocess, json, requests
from EventFlow.ThreadDaemon import ThreadDaemon

name = 'ResourceCollector'
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

class ResourceCollector(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.before_time = None
        self.prev_system_cpu_jiffy = []
        self.value_list = {}

    def _system_cpu_info(self, time_info):
        cpu_data = psutil.cpu_times()
        if time_info not in self.value_list: self.value_list[time_info] = {}
        if 'system' not in self.value_list[time_info]: self.value_list[time_info]['system'] = {}
        if 'cpu' not in self.value_list[time_info]['system']: self.value_list[time_info]['system']['cpu'] = {}
        if len(self.prev_system_cpu_jiffy) == 0:
            self.prev_system_cpu_jiffy.append(cpu_data.system)
            self.prev_system_cpu_jiffy.append(cpu_data.user)
            self.prev_system_cpu_jiffy.append(cpu_data.idle)
            self.value_list[time_info]['system']['cpu']['system'] = '-'
            self.value_list[time_info]['system']['cpu']['user'] = '-'
            self.value_list[time_info]['system']['cpu']['idle'] = '-'
        else:
            system_jiffy = cpu_data.system - self.prev_system_cpu_jiffy[0]
            user_jiffy = cpu_data.user - self.prev_system_cpu_jiffy[1]
            idle_jiffy = cpu_data.idle - self.prev_system_cpu_jiffy[2]
            total_jiffy = system_jiffy + user_jiffy + idle_jiffy
            self.prev_system_cpu_jiffy[0] = cpu_data.system
            self.prev_system_cpu_jiffy[1] = cpu_data.user
            self.prev_system_cpu_jiffy[2] = cpu_data.idle
            self.value_list[time_info]['system']['cpu']['system'] = \
                float(system_jiffy) / float(total_jiffy) * 100
            self.value_list[time_info]['system']['cpu']['user'] = \
                float(user_jiffy) / float(total_jiffy) * 100
            self.value_list[time_info]['system']['cpu']['idle'] = \
                float(idle_jiffy) / float(total_jiffy) * 100

    def _system_memory_info(self, time_info):
        memory_data = psutil.virtual_memory()
        swap_data = psutil.swap_memory()
        if time_info not in self.value_list: self.value_list[time_info] = {}
        if 'system' not in self.value_list[time_info]: self.value_list[time_info]['system'] = {}
        if 'memory' not in self.value_list[time_info]['system']: self.value_list[time_info]['system']['memory'] = {}
        if 'swap' not in self.value_list[time_info]['system']: self.value_list[time_info]['system']['swap'] = {}
        self.value_list[time_info]['system']['memory']['total'] = memory_data.total
        self.value_list[time_info]['system']['memory']['available'] = memory_data.available
        self.value_list[time_info]['system']['swap']['total'] = swap_data.total
        self.value_list[time_info]['system']['swap']['available'] = swap_data.free

    def _system_disk_info(self, time_info):
        if time_info not in self.value_list: self.value_list[time_info] = {}
        if 'system' not in self.value_list[time_info]: self.value_list[time_info]['system'] = {}
        if 'disk' not in self.value_list[time_info]['system']: self.value_list[time_info]['system']['disk'] = {}
        ignore_list = [ 'Filesystem', 'tmpfs', 'hugetlbfs', 'cgroup', 'udev', 'sysfs', 'proc' ]
        pd = subprocess.Popen("/bin/df -l", shell=True, stdout=subprocess.PIPE)
        total = 0
        t_available = 0
        for line in pd.stdout:
            try: file_system_type, _, used, available, _, mount = line.strip().split()
            except: continue
            if file_system_type in ignore_list: continue
            total = total + ( int(used) + int(available) )
            t_available = t_available + int(available)
        pd.wait()
        self.value_list[time_info]['system']['disk']['total'] = total
        self.value_list[time_info]['system']['disk']['available'] = t_available

    def get_last_data(self):
        key_list = self.value_list.keys()
        key_list.sort()
        try:return self.value_list[key_list[-1]]
        except: return None

    def make_resource_data(self, data):
        temp_hash = {}
        try:
            temp_hash['data'] = {}
            try: temp_hash['data']['cpu_usage'] = str( float(data['system']['cpu']['system']) + float(data['system']['cpu']['user'] ))
            except Exception, e: 
                exceptionLog(str(e))
                temp_hash['data']['cpu_usage'] = '-'
            try: temp_hash['data']['ram_usage'] = str( float(data['system']['memory']['total'] - data['system']['memory']['available']) / data['system']['memory']['total'] * 100 )
            except Exception, e: 
                exceptionLog(str(e))
                temp_hash['data']['ram_usage'] = '-'
            try: temp_hash['data']['disk_usage'] = str( float(data['system']['disk']['total'] - data['system']['disk']['available']) / data['system']['disk']['total'] * 100 )
            except Exception, e: 
                exceptionLog(str(e))
                temp_hash['data']['disk_usage'] = '-'
            try:temp_hash['data']['datetime'] = time.strftime('%Y%m%d%H%M00', time.localtime(time.time()))
            except Exception, e: 
                exceptionLog(str(e))
                temp_hash['data']['datetime'] = '-'
        except Exception, e: 
            exceptionLog(str(e))
            return {}
        return temp_hash
    
    def send_resource_data(self, data):
        if not self.main_p.announcer_run: return
        url = '%s:%s%s' % ( self.main_p.announcer_dst_addr, self.main_p.announcer_dst_port, self.main_p.announcer_resource_api )
        json_data = json.dumps(self.make_resource_data(data), indent=4)
        if not url.startswith('http'): url = 'http://' + url
        if self.debugMode:debugLog(url)
        if self.debugMode:debugLog(json_data)
        try:
            res = requests.post(url, headers={'Content-Type':'application/json'}, data=json_data)
            if self.debugMode:debugLog('result data send result : %s' % str(res) )
        except Exception, e:
            if self.debugMode:debugLog('result data send failed [%s]' % str(e))

    def loop(self):
        time_string = time.strftime('%Y%m%d%H%M00', time.localtime())
        if not self.before_time:
            self.before_time = time_string
        if self.before_time == time_string:
            self.before_time = time_string
            return

        self._system_cpu_info(time_string)
        self._system_memory_info(time_string)
        self._system_disk_info(time_string)

        self.before_time = time_string
        if len(self.value_list) >= self.main_p.resource_monitor_size:
            key_list = self.value_list.keys()
            key_list.sort()
            del self.value_list[key_list[0]]
            if self.debugMode: debugLog(str(self.value_list[key_list[-1]]))

        if self.debugMode: debugLog("current queue size : %d" % len(self.value_list.keys()))
        data = self.get_last_data()
        self.send_resource_data(data)

