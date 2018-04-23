import sys, time, signal, collections, os, random, string
import WorkFlow.Common.Conf.Default                                       as DefaultConfig

#import WorkFlow.Conf.DatabaseHelper                                as DBHelper
#from WorkFlow.Conf.ConfigDatabase      import ConfigDatabase       as ConfigDB
#from WorkFlow.Conf.NodeDatabase        import NodeDatabase         as NodeDB
#from WorkFlow.Conf.FlowDatabase        import FlowDatabase         as FlowDB
#from WorkFlow.Conf.ScheduleDatabase    import ScheduleDatabase     as ScheduleDB
#from WorkFlow.Conf.GroupDatabase       import GroupDatabase        as GroupDB

#from WorkFlow.Core                     import Core
#from WorkFlow.ConsoleListener          import ConsoleListener
#from WorkFlow.Scheduler                import Scheduler
#from WorkFlow.WebListener              import WebListener
#from WorkFlow.WebMonitor               import WebMonitor
#from WorkFlow.ResourceCollector        import ResourceCollector
#from WorkFlow.ResultCollector          import ResultCollector
#from WorkFlow.MiddleInterface import MiddleInterface


import WorkFlow.Common.Log as Log
from WorkFlow.Common.Log import __LOG__
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

# WFManager MainProcessor
# This class run in front of WorkFlow
# Manage all Manger daemon 
class WFManager:
    def __init__(self, name, debugMode=True, host='127.0.0.1', port=9999):
        # init name and default configuration
        self.name = name
        self.debugMode = debugMode
        self.host = host
        self.port = port

        # load default env
        self.home_path = DefaultConfig.WORKFLOW_HOME
        if not self.home_path:
            raise Exception, "WORKFLOW HOME IS NOT SETTED!"
            sys.exit(1)

        # shutdown flag set and set signal handler
        self.shutdownFlag = False
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)

        # init default database
        #self.config_conn     = ConfigDB(self.name)
        #self.node_conn       = NodeDB(self.name)
        #self.flow_conn       = FlowDB(self.name)
        #self.schedule_conn   = ScheduleDB(self.name)
        #self.group_conn      = GroupDB(self.name)

        # init daemon list
        # share this daemon with parent class follow
        self.daemon_list = {}
        #self.daemon_list[Core.__name__] = Core
        #self.daemon_list[ConsoleListener.__name__] = ConsoleListener
        #self.daemon_list[Scheduler.__name__] = Scheduler
        #self.daemon_list[WebListener.__name__] = WebListener
        #self.daemon_list[WebMonitor.__name__] = WebMonitor
        #self.daemon_list[ResourceCollector.__name__] = ResourceCollector
        #self.daemon_list[ResultCollector.__name__] = ResultCollector

        #self.middle_interface = MiddleInterface(self, web=False)

        #try: self.max_mon_deque_size = int(self.config_conn.get_by_key('max monitoring deque size')[1])
        #except: self.max_mon_deque_size = 1000
        #try: self.max_save_deque_size = int(self.config_conn.get_by_key('max save deque size')[1])
        #except: self.max_save_deque_size = 1000
        #try: self.error_data_file_skip = ( self.config_conn.get_by_key('error data file skip')[1].upper() == 'TRUE' )
        #except: self.error_data_file_skip = False 
        #try: self.max_cmd_queue_size = int(self.config_conn.get_by_key('max cmd queue size')[1])
        #except: self.max_cmd_queue_size = 100000
        #try: self.kill_wait_time = int(self.config_conn.get_by_key('kill wait time')[1])
        #except: self.kill_wait_time = 10
        #try: self.save_event_file_path = self.config_conn.get_by_key('event save file')[1]
        #except: self.save_event_file_path = '/dev/null'

        #try : self.scheduler_run = ( self.config_conn.get_by_key('scheduler run')[1].upper() == 'TRUE' )
        #except: self.scheduler_run = False

        #try: self.flask_run = ( self.config_conn.get_by_key('flask run')[1].upper() == 'TRUE' )
        #except: self.flask_run = False
        #try: self.flask_port = int(self.config_conn.get_by_key('flask port')[1])
        #except: self.flask_port = 5000
        #try: self.flask_shutdown_code = '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
        #except: self.flask_shutdown_code = '/shutdown'

        #try: self.resource_monitor_size = int(self.config_conn.get_by_key('resource monitor size')[1])
        #except: self.resource_monitor_size = 10
        #try: self.result_monitor_size = int(self.config_conn.get_by_key('result monitor size')[1])
        #except: self.result_monitor_size = 10

        #try: self.announcer_run = ( self.config_conn.get_by_key('announcer run')[1].upper() == 'TRUE' )
        #except: self.announcer_run = False
        #try: self.announcer_dst_addr = self.config_conn.get_by_key('announcer dst address')[1]
        #except: self.announcer_dst_addr = '127.0.0.1'
        #try: self.announcer_dst_port = int(self.config_conn.get_by_key('announcer dst port')[1])
        #except: self.announcer_dst_port = 8888
        #try: self.announcer_result_api = self.config_conn.get_by_key('announcer result api')[1]
        #except: self.announcer_result_api = '/api/v1/worker/%s/jobs' % self.name
        #try: self.announcer_resource_api = self.config_conn.get_by_key('announcer resource api')[1]
        #except: self.announcer_resource_api = '/api/v1/worker/%s/resources' % self.name
        #try: self.announcer_alert_api = self.config_conn.get_by_key('announcer alert api')[1]
        #except: self.announcer_alert_api = '/api/v1/worker/%s/alert' % self.name

        #try: self.recovery_time_out = int(self.config_conn.get_by_key('recovery time out')[1])
        #except: self.recovery_time_out = 3600
        #try: self.recovery_del_time = int(self.config_conn.get_by_key('recovery delete time')[1])
        #except: self.recovery_del_time = 3600 * 24

        #try: self.work_directory = self.config_conn.get_by_key('work directory')[1]
        #except: self.work_directory = self.home_path + '/work/' + self.name
        #try: os.makedirs(self.work_directory)
        #except: pass
          

        #self.mon_deque = collections.deque([], self.max_mon_deque_size)
        #self.save_deque = collections.deque([], self.max_save_deque_size)

        # initializing each daemon
        self.thread_daemon_list = {}
        #for name in self.daemon_list:
        #    self.thread_daemon_list[name] = self.daemon_list[name](self, debugMode=self.debugMode)

    #def config_reload(self):
        #try: self.max_mon_deque_size = int(self.config_conn.get_by_key('max monitoring deque size')[1])
        #except: self.max_mon_deque_size = 1000
        #try: self.max_save_deque_size = int(self.config_conn.get_by_key('max save deque size')[1])
        #except: self.max_save_deque_size = 1000
        #try: self.error_data_file_skip = ( self.config_conn.get_by_key('error data file skip')[1].upper() == 'TRUE' )
        #except: self.error_data_file_skip = False 
        #try: self.max_cmd_queue_size = int(self.config_conn.get_by_key('max cmd queue size')[1])
        #except: self.max_cmd_queue_size = 100000
        #try: self.kill_wait_time = int(self.config_conn.get_by_key('kill wait time')[1])
        #except: self.kill_wait_time = 10
        #try: self.save_event_file_path = self.config_conn.get_by_key('event save file')[1]
        #except: self.save_event_file_path = '/dev/null'

        #try : self.scheduler_run = ( self.config_conn.get_by_key('scheduler run')[1].upper() == 'TRUE' )
        #except: self.scheduler_run = False

        #try: self.flask_run = ( self.config_conn.get_by_key('flask run')[1].upper() == 'TRUE' )
        #except: self.flask_run = False
        #try: self.flask_port = int(self.config_conn.get_by_key('flask port')[1])
        #except: self.flask_port = 5000

        #try: self.resource_monitor_size = int(self.config_conn.get_by_key('resource monitor size')[1])
        #except: self.resource_monitor_size = 10
        #try: self.result_monitor_size = int(self.config_conn.get_by_key('result monitor size')[1])
        #except: self.result_monitor_size = 10

        #try: self.announcer_run = ( self.config_conn.get_by_key('announcer run')[1].upper() == 'TRUE' )
        #except: self.announcer_run = False
        #try: self.announcer_dst_addr = self.config_conn.get_by_key('announcer dst address')[1]
        #except: self.announcer_dst_addr = '127.0.0.1'
        #try: self.announcer_dst_port = int(self.config_conn.get_by_key('announcer dst port')[1])
        #except: self.announcer_dst_port = 8888
        #try: self.announcer_result_api = self.config_conn.get_by_key('announcer result api')[1]
        #except: self.announcer_result_api = '/api/v1/worker/%s/jobs' % self.name
        #try: self.announcer_resource_api = self.config_conn.get_by_key('announcer resource api')[1]
        #except: self.announcer_resource_api = '/api/v1/worker/%s/resources' % self.name
        #try: self.announcer_alert_api = self.config_conn.get_by_key('announcer alert api')[1]
        #except: self.announcer_alert_api = '/api/v1/worker/%s/alert' % self.name
        #try: self.recovery_time_out = int(self.config_conn.get_by_key('recovery time out')[1])
        #except: self.recovery_time_out = 3600
        #try: self.recovery_del_time = int(self.config_conn.get_by_key('recovery delete time')[1])
        #except: self.recovery_del_time = 3600 * 24

        #try: self.work_directory = self.config_conn.get_by_key('work directory')[1]
        #except: self.work_directory = self.home_path + '/work/' + self.name
        #try: os.makedirs(self.work_directory)
        #except: pass

    #def start_all_saved_task(self):
    #    task_list = self.node_conn.lst()
    #    for item in task_list:
    #        self.thread_daemon_list['Core'].add_task( item[0], item[1], item[2] )
    #        while not self.thread_daemon_list['Core'].check_task_ready(item[1]): time.sleep(1)

    #def set_all_saved_flow(self):
    #    flow_list = self.flow_conn.lst()
    #    for item in flow_list:
    #        self.thread_daemon_list['Core'].add_flow( item[0], item[1], item[2] )

    #def set_all_saved_group(self):
    #    group_list = self.group_conn.lst()
    #    for item in group_list:
    #        self.thread_daemon_list['Core'].add_group( item[0], item[1] )

    # for signal handling
    def sig_handler(self, sigNum, frame) :
        self.shutdownFlag = True
        if self.debugMode: debugLog("signal %d detected" % sigNum)
        self._all_thread_kill()

    # call shutdown function
    def shutdown(self):
        self.shutdownFlag = True
        if self.debugMode: debugLog("shutdown called")
        self._all_thread_kill()

    # kill all thread
    def _all_thread_kill(self):
        for name in self.thread_daemon_list:
            try:
                if self.debugMode:debugLog("kill start %s" % name)
                self.thread_daemon_list[name].shutdown()
                self.thread_daemon_list[name].join()
                if self.debugMode:debugLog("kill end %s" % name )
            except:pass

    # run all thread
    def _run_thread(self):
        for name in self.thread_daemon_list:
            if not self.thread_daemon_list[name].is_alive():
                #if self.thread_daemon_list[name].firstRun:
                #    if self.debugMode: debugLog("%s daemon fail detected. re initializing" % name)
                #    self.thread_daemon_list[name] = self.daemon_list[name](self, debugMode=self.debugMode)
                #if self.debugMode: debugLog("%s daemon stop detected. start it" % name)
                self.thread_daemon_list[name].start()
    
    # if shutdown flag is False, then check each daemon every 1 sec
    def run(self):
        self._run_thread()
        #self.start_all_saved_task()
        #self.set_all_saved_flow()
        #self.set_all_saved_group()
        while True:
            if self.shutdownFlag:
                break
            self._run_thread()
            time.sleep(1)

if __name__ == '__main__':
    #Log.Init()
    wfm = WFManager("TEST", debugMode=True)
    wfm.run()



