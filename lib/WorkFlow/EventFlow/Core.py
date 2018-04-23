import importlib, time, threading
from EventFlow.ThreadDaemon import ThreadDaemon

name = 'Core'
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



class Core(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        self.main_p = main_process
        # list for waiting
        self.act_list = []
        self.trm_list = []
        self.add_list = []
        self.del_list = []
        self.recover_list = []
 
        # for all task object
        self.all_task_object = {}

        # for all recovery task object
        self.all_recovery_object = {}

        # delete task wait list
        self.deleted_task = []

        # flow dict
        self.all_broad_flow = {}
        self.all_share_flow = {}

        self.all_group = {}

        self.runner_thread = None

        self.recovery_result = {}

    def shutdown(self):
        for name in self.all_task_object:
            self.all_task_object[name].shutdown()
            self.all_task_object[name].join()
        for name in self.all_recovery_object:
            self.all_recovery_object[name].shutdown()
            self.all_recovery_object[name].join()
        if self.debugMode: debugLog("%s daemon shutdown called" % self.__class__.__name__)
        self.shutdownFlag = True
        normalLog("%s daemon shutdown flag setted" % self.__class__.__name__)

    def add_group(self, group_name, task_name):
        try:
            if task_name not in self.all_task_object: raise Exception, "[%s] task not exsits" % task_name
            if group_name not in self.all_group: self.all_group[group_name] = []
            if task_name in self.all_group[group_name]: raise Exception, "[%s] task is already exists in group [%s]" % (task_name, group_name)
            self.all_group[group_name].append(task_name)
        except Exception, e:
            return [ 'NOK : %s' % str(e) ]
        return [ 'OK : [%s] task add to group [%s]' % (task_name, group_name) ]

    def del_group(self, group_name, task_name):
        try:
            if task_name not in self.all_task_object: raise Exception, '[%s] task not exists' % task_name
            if not group_name:
                ret_list = []
                for temp_group_name in self.all_group:
                    if task_name in self.all_group[temp_group_name]: 
                        for line in self.del_group(temp_group_name, task_name):
                            ret_list.append(line)
                if len(ret_list) == 0:
                    return [ 'NOK : [%s] task not associated any group' % task_name ]
                else:
                    return ret_list
            else:
                if group_name not in self.all_group: raise Exception, '[%s] group not exists' % group_name
                self.all_group[group_name].remove(task_name)

            for temp_group_name in self.all_group.keys():
                if len(self.all_group[temp_group_name]) == 0: del self.all_group[temp_group_name]

        except Exception, e:
            return [ 'NOK : %s' % str(e) ]
        return [ 'OK : [%s] task del from group [%s]' % (task_name, group_name) ]


    def add_flow(self, flow_type, flow_from, flow_to):
        flow_reset_task = []
        try:
            if flow_from not in self.all_task_object.keys(): raise Exception, "[%s] task not exists" % flow_from
            if flow_to not in self.all_task_object.keys(): raise Exception, "[%s] task not exists" % flow_to
            if flow_type.lower() == 'broad':
                if self.all_task_object[flow_to] in self.all_task_object[flow_from].broadcast_task_list: raise Exception, "%s flow, %s -> %s already exists" % (flow_type, flow_from, flow_to)
                self.all_task_object[flow_from].broadcast_task_list.append(self.all_task_object[flow_to])
                if flow_from not in flow_reset_task: flow_reset_task.append(flow_from)
                if flow_from not in self.all_broad_flow: self.all_broad_flow[flow_from] = []
                self.all_broad_flow[flow_from].append(flow_to)
            elif flow_type.lower() == 'share': 
                if self.all_task_object[flow_from] in self.all_task_object[flow_to].sharing_task_list: raise Exception, "%s flow, %s -> %s already exists" % (flow_type, flow_from, flow_to)
                self.all_task_object[flow_to].sharing_task_list.append(self.all_task_object[flow_from])
                self.all_task_object[flow_from].out_deq = True
                if flow_to not in flow_reset_task: flow_reset_task.append(flow_to)
                if flow_from not in flow_reset_task: flow_reset_task.append(flow_from)
                if flow_from not in self.all_share_flow: self.all_share_flow[flow_from] = []
                self.all_share_flow[flow_from].append(flow_to)
            else: raise Exception, "unknown flow type [%s]" % flow_type
        except Exception,e:
            return [ 'NOK : %s\n' % str(e) ]
        for task_name in flow_reset_task:
            self.all_task_object[task_name].set_flow()
        return [ 'OK : %s, %s -> %s is setted\n' % (flow_type, flow_from, flow_to) ]

    def del_flow(self, flow_type, flow_from, flow_to):
        flow_reset_task = []
        try:
            if flow_from not in self.all_task_object: raise Exception, "[%s] task not exists" % flow_from
            if flow_to not in self.all_task_object: raise Exception, "[%s] task not exists" % flow_to
            if flow_type.lower() == 'broad':
                if self.all_task_object[flow_to] not in self.all_task_object[flow_from].broadcast_task_list: raise Exception, "%s flow, %s -> %s not exists" % (flow_type, flow_from, flow_to)
                self.all_task_object[flow_from].broadcast_task_list.remove(self.all_task_object[flow_to])
                if flow_from not in flow_reset_task: flow_reset_task.append(flow_from)
                if flow_to in self.all_broad_flow[flow_from]: self.all_broad_flow[flow_from].remove(flow_to)
            elif flow_type.lower() == 'share': 
                if self.all_task_object[flow_from] not in self.all_task_object[flow_to].sharing_task_list: raise Exception, "%s flow, %s -> %s not exists" % (flow_type, flow_from, flow_to)
                self.all_task_object[flow_to].sharing_task_list.remove(self.all_task_object[flow_from])
                out_deq_check = False
                if flow_to in self.all_share_flow[flow_from]: self.all_share_flow[flow_from].remove(flow_to)
                if len(self.all_share_flow[flow_from]) == 0: self.all_task_object[flow_from].out_deq = False
                if flow_to not in flow_reset_task: flow_reset_task.append(flow_to)
                if flow_from not in flow_reset_task: flow_reset_task.append(flow_from)
            else: raise Exception, "unknown flow type [%s]" % flow_type
        except Exception,e:
            return [ 'NOK : %s\n' % str(e) ]
        for task_name in flow_reset_task:
            self.all_task_object[task_name].set_flow()
        return [ 'OK : %s, %s -> %s is deleted\n' % (flow_type, flow_from, flow_to) ]
    
    def act_task(self, task_name):
        try:
            if task_name not in self.all_task_object: 
                if task_name in self.all_group:
                    ret_list = []
                    for second_task_name in self.all_group[task_name]:
                        ret = self.act_task(second_task_name)
                        for line in ret:
                            ret_list.append(line)
                    return ret_list
                elif task_name.lower() == 'all':
                    ret_list = []
                    for second_task_name in self.all_task_object:
                        ret = self.act_task(second_task_name)
                        for line in ret:
                            ret_list.append(line)
                    return ret_list
                else: raise Exception, "[%s] task not exists" % task_name
            if task_name not in self.act_list: self.act_list.append(task_name)
        except Exception, e:
            return [ 'NOK : %s\n' % str(e) ]
        return  [ 'OK : [%s] task set to act\n' % task_name ]

    def trm_task(self, task_name):
        try:
            if task_name not in self.all_task_object:
                if task_name in self.all_group:
                    ret_list = []
                    for second_task_name in self.all_group[task_name]:
                        ret = self.trm_task(second_task_name)
                        for line in ret:
                            ret_list.append(line)
                    return ret_list
                elif task_name.lower() == 'all':
                    ret_list = []
                    for second_task_name in self.all_task_object:
                        ret = self.trm_task(second_task_name)
                        for line in ret:
                            ret_list.append(line)
                    return ret_list
                else: raise Exception, "[%s] task not exists" % task_name
            if task_name not in self.trm_list: self.trm_list.append(task_name)
        except Exception, e:
            return [ 'NOK : %s\n' % str(e) ]
        return  [ 'OK : [%s] task set to trm\n' % task_name ]
    
    def add_task(self, task_type, task_name, task_command):
        try:
            if task_name in self.all_task_object.keys() + self.add_list: raise Exception, "[%s] task already exists" % task_name
            self.add_list.append( (task_type, task_name, task_command) )
        except Exception, e:
            return [ 'NOK : %s\n' % str(e) ]
        return  [ 'OK : [%s] task set to add\n' % task_name ]
   
    def add_recovery(self, task_name, message):
        try:
            if task_name not in self.all_task_object: raise Exception, "[%s] task not exiests" % task_name
            task_type = self.all_task_object[task_name].status['type']
            task_command = self.all_task_object[task_name].status['command']
            if task_name in self.all_recovery_object.keys() + self.recover_list: raise Exception, "[%s] task already in recovery mode" % task_name
            self.recover_list.append( (task_type, task_name, task_command, message) )
        except Exception, e:
            return [ 'NOK : %s\n' % str(e) ]
        return  [ 'OK : [%s] task set to recover\n' % task_name ]

    def del_task(self, task_name):
        try:
            if task_name not in self.all_task_object.keys() + self.add_list: raise Exception, "[%s] task not exists" % task_name
            if task_name not in self.del_list: self.del_list.append(task_name)
        except Exception, e:
            return [ 'NOK : %s\n' % str(e) ]
        return  [ 'OK : [%s] task set to del\n' % task_name ]

    def _task_trm_runner(self):
        if len(self.trm_list) == 0: return False
        try:
            task_name = self.trm_list.pop()
            if self.all_task_object[task_name].status['status'] == 'ACT':
                self.all_task_object[task_name].trm()
                return False
            return True
        except Exception, e:
            exceptionLog("[%s] task trm failed. : %s" % (task_name, str(e)))
        return True

    def _task_act_runner(self):
        if len(self.act_list) == 0: return False
        try:
            task_name = self.act_list.pop()
            self.all_task_object[task_name].act()
            return False
        except Exception, e:
            exceptionLog("[%s] task act failed. : %s" % (task_name, str(e)))
        return True

    def check_task_ready(self, task_name):
        if task_name not in self.all_task_object: return False
        return True

    def _task_add_runner(self):
        if len(self.add_list) == 0: return False
        try:
            task_type, task_name, task_command = self.add_list.pop()

            task_type = task_type.upper()[0] + task_type.lower()[1:]
            task_module = importlib.import_module("EventFlow.Task.%sTask" % task_type)
            task_class = getattr(task_module, '%sTask' % task_type)

            if task_name in self.all_task_object: raise Exception, "[%s] task already exists. exception occured in background adder" % task_name

            self.all_task_object[task_name] = task_class(task_name, task_command, self.main_p, debugMode=self.debugMode)
            self.all_task_object[task_name].set_flow()
            self.all_task_object[task_name].daemon = True
            self.all_task_object[task_name].start()
            return False
            
        except Exception, e:
            try: self.add_list.append( (task_type, task_name, task_command) )
            except: pass
            exceptionLog("[%s] task add failed. : %s" % (task_name, str(e)))
            return False
        return True

    def _task_recovery_runner(self):
        del_name = []
        for task_name in self.recovery_result:
            if self.recovery_result[task_name][1] == '-': continue
            if self.recovery_result[task_name][1] < time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() - self.main_p.recovery_del_time)):
                del_name.append(task_name)
            if self.recovery_result[task_name][1] in ['FAIL', 'TIME_OUT']:
                if self.recovery_result[task_name][1] < time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() - self.main_p.recovery_del_time)):
                    del_name.append(task_name)
        for name in del_name:
            del self.recovery_result[name]
        
        for task_name in self.all_recovery_object.keys():
            if self.all_recovery_object[task_name].status['status'] == 'TRM' and \
                self.all_recovery_object[task_name].status['act-status'] == 'OK':
                del self.all_recovery_object[task_name]
                continue
            if not self.all_recovery_object[task_name].is_alive():
                del self.all_recovery_object[task_name]
            else:
                recovery_name = self.all_recovery_object[task_name].recovery_name
                time_info = recovery_name.rsplit('-', 1)[-1]
                if self.recovery_result[recovery_name][0] < time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() - self.main_p.recovery_time_out)):
                    self.all_recovery_object[task_name].trm()
                    self.recovery_result[recovery_name][1] = 'TIME_OUT'
                
        if len(self.recover_list) == 0: return False
        try:
            task_type, task_name, task_command, message = self.recover_list.pop()

            task_type = task_type.upper()[0] + task_type.lower()[1:]
            task_module = importlib.import_module("EventFlow.Task.%sTask" % task_type)
            task_class = getattr(task_module, '%sTask' % task_type)

            self.all_recovery_object[task_name] = task_class(task_name, task_command, self.main_p, debugMode=self.debugMode, recoveryMode=True)
            self.all_recovery_object[task_name].set_flow()
            
            self.all_recovery_object[task_name].daemon = True
            self.all_recovery_object[task_name].start()

            ready_count = 0
            while True:
                if self.all_recovery_object[task_name].status['status'] == 'ACT' and \
                    self.all_recovery_object[task_name].status['act-status'] == 'OK': break
                if ready_count == 10:
                    self.all_recovery_object[task_name].trm()
                    del self.all_recovery_object[task_name]
                    self.recovery_result[recovery_name] = [ time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())), 'FAIL' ]
                    raise Exception, "10 retry expired [%s] add again."
                ready_count += 1
                time.sleep(0.1)

            self.all_recovery_object[task_name].put_queue(message)
            start_time = time.time()
            recovery_name = task_name + '-' + message + '-' + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            
            self.recovery_result[recovery_name] = [ time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())), '-' ]
            self.all_recovery_object[task_name].set_recovery_name(recovery_name)

            return False
        except Exception, e:
            exceptionLog("[%s] task recovery failed. : %s" % (task_name, str(e)))
            return False
        return False
            

    def _task_del_runner(self):
        while True:
            if len(self.deleted_task) == 0: break
            del_task = self.deleted_task.pop()
            if del_task.status['status'] == 'ACT': 
                del_task.trm()
                self.deleted_task.append(del_task)
                return False
            try:
                task_type_temp = del_task.status['type']
                task_type = task_type_temp[0].upper() + task_type_temp[1:].lower()
                task_module = importlib.import_module("EventFlow.Task.%sTask" % task_type)
                task_class = getattr(task_module, '%sTaskDelHelper' % task_type)(self.main_p, del_task.status['name']) 
                task_class.run()
            except Exception, e:
                exceptionLog("[%s] task delete helper faile [%s]" % (del_task.status['name'], str(e)))
        if len(self.del_list) == 0: return False
        try:
            task_name = self.del_list.pop()
            for from_task in self.all_broad_flow:
                for to_task in self.all_broad_flow[from_task]:
                    if from_task == task_name or to_task == task_name:
                        self.main_p.middle_interface.command("del flow %s:%s:%s" % ('broad', from_task, to_task ))
            for from_task in self.all_share_flow:
                for to_task in self.all_share_flow[from_task]:
                    if from_task == task_name or to_task == task_name:
                        self.main_p.middle_interface.command("del flow %s:%s:%s" % ('share', from_task, to_task ))

            for group_name in self.all_group.keys()[:]:
                if task_name in self.all_group[group_name]:
                    self.main_p.middle_interface.command('del group %s:%s' % ( group_name, task_name ) )

            self.main_p.schedule_conn.rmv_by_task(task_name)
                        
            self.deleted_task.append(self.all_task_object[task_name])
            del self.all_task_object[task_name]


            return True
        except Exception, e:
            exceptionLog("[%s] task delete failed. : %s" % (task_name, str(e)))
        return True

    def get_task(self, name):
        if name not in self.all_task_object: return None
        return self.all_task_object[name]
        
    def loop(self):
        while self._task_add_runner():continue
        while self._task_del_runner():continue
        while self._task_act_runner():continue
        while self._task_trm_runner():continue
        while self._task_recovery_runner():continue

if __name__ == '__main__':
    core = Core(None)
    core.act_set('test')
