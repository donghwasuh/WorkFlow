import json
import EventFlow.MessageFormatter as MF

import EventFlow.Interface.Config   as ConfigInterface
import EventFlow.Interface.Task     as TaskInterface
import EventFlow.Interface.StdIn    as StdInInterface
import EventFlow.Interface.Flow     as FlowInterface
import EventFlow.Interface.Group    as GroupInterface
import EventFlow.Interface.Schedule as ScheduleInterface
import EventFlow.Interface.Queue    as QueueInterface
import EventFlow.HelpMessageCenter as HLPMessage


import EventFlow.Log as Log
Log.Init()

class MiddleInterface:
    def __init__(self, main_p, web=False):
        self.main_p = main_p
        self.web = web

    def command(self, line):
        command_data = line.strip().split()


        if command_data[-1].lower() == 'hlp':
            try: 
                if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), command_data[1].lower()))
            except:
                try:
                    if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), None))
                except:
                    if not self.web: return MF.make_message(HLPMessage.help_msg('hlp', None))

        if len(command_data) == 1 and command_data[0].lower() in [ 'shw', 'set', 'del' ]:
            if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), None))

        if command_data[0].lower() == 'shw':
            if command_data[1].lower() == 'conf':
                return ConfigInterface.shw_conf(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'task':
                return TaskInterface.shw_task(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'flow':
                return FlowInterface.shw_flow(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'group':
                return GroupInterface.shw_group(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'stdin':
                return StdInInterface.shw_stdin(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'schedule':
                return ScheduleInterface.shw_schedule(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'global_queue':
                return QueueInterface.shw_global_queue(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'status':
                return TaskInterface.shw_status(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'recovery':
                return TaskInterface.shw_recovery(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'ready':
                return TaskInterface.shw_ready(self.main_p, command_data, web=self.web)
            else:
                if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), None))

        elif command_data[0].lower() == 'set':
            if command_data[1].lower() == 'conf':
                return ConfigInterface.set_conf(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'task':
                return TaskInterface.set_task(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'flow':
                return FlowInterface.set_flow(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'group':
                return GroupInterface.set_group(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'stdin':
                return StdInInterface.set_stdin(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'schedule':
                return ScheduleInterface.set_schedule(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'recovery':
                return TaskInterface.set_recovery(self.main_p, command_data, web=self.web)
            else:
                if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), None))

        elif command_data[0].lower() == 'del':
            if command_data[1].lower() == 'task':
                return TaskInterface.del_task(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'flow':
                return FlowInterface.del_flow(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'group':
                return GroupInterface.del_group(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'schedule':
                return ScheduleInterface.del_schedule(self.main_p, command_data, web=self.web)
            elif command_data[1].lower() == 'task_queue':
                return QueueInterface.del_task_queue(self.main_p, command_data, web=self.web)
            else:
                if not self.web: return MF.make_message(HLPMessage.help_msg(command_data[0].lower(), None))

        elif command_data[0].lower() == 'act':
            return TaskInterface.act_task(self.main_p, command_data, web=self.web)
        elif command_data[0].lower() == 'trm':
            return TaskInterface.trm_task(self.main_p, command_data, web=self.web)

        elif command_data[0].lower() == 'lad':
            return QueueInterface.lad_task_queue(self.main_p, command_data, web=self.web)
        elif command_data[0].lower() == 'sav':
            return QueueInterface.sav_task_queue(self.main_p, command_data, web=self.web)

        if not self.web: return MF.make_message(HLPMessage.help_msg('hlp', None))
        else: return MF.make_json( { 'RESULT' : 'NOK', 'MESSAGE' : 'unknown command [%s]' % repr(line) } )
