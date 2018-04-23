import json
import EventFlow.MessageFormatter as MF
from EventFlow.Interface.OptParserForTask import OptParserForTask as OptionParser
from EventFlow.Interface.OptParserForTask import OptionParsingError

def shw_group(main_p, command_data, web=False):
    try:
        parser = OptionParser()
        parser.add_option('-g', '--group', dest='group')
        parser.add_option('-t', '--task', dest='task')
        options, _ = parser.parse_args(command_data)
    except OptionParsingError, e:
        error_msg = 'NOK : shw group option error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
    def view_check(options, data, message):
        if options.group != None and data[0] not in options.group: return message
        if options.task != None:
            return_check = False
            for task_name in options.task:
                if task_name in data[1]: return_check = True
            if not return_check: return message
        message.append( ( data[0], ','.join(data[1]) ) )
        return message
    try:
        core_obj = main_p.thread_daemon_list['Core']
        group_item = core_obj.all_group
        result_list = []
        for item in group_item:
            result_list = view_check(options, (item, group_item[item]), result_list)
        if not web: return MF.shw_group_list(result_list)
        else: return MF.simple_result_json(result_list, header='GROUPS', column=[ 'GROUP_NAME', 'TASK_LIST' ])
    except Exception, e:
        error_msg = "NOK : Excetpion occured in shw group [%s]" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json([error_msg])

def set_group(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        core_obj = main_p.thread_daemon_list['Core']
        for command in map(lambda x:x.strip(), command_string.split(',')):
            group_name_list, task_name_list = map(lambda x:x.strip(), command.split(':'))
            for group_name in map(lambda x:x.strip(), group_name_list.split('|')):
                for task_name in map(lambda x:x.strip(), task_name_list.split('|')):
                    ret = core_obj.add_group(group_name, task_name)
                    for line in ret:
                        return_message.append(line)
                    try:
                        main_p.group_conn.set(group_name, task_name)
                    except Exception, e:
                        return_message.append("NOK : Exception in set group save [%s]" % str(e))
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Excetpion occured in set group [%s]" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json([error_msg])

def del_group(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        core_obj = main_p.thread_daemon_list['Core']
        for command in map(lambda x:x.strip(), command_string.split(',')):
            try: 
                group_name_list, task_name_list = map(lambda x:x.strip(), command.split(':'))
            except:
                group_name_list = command.strip()
                task_name_list = None
            for group_name in map(lambda x:x.strip(), group_name_list.split('|')):
                if task_name_list:
                    for task_name in map(lambda x:x.strip(), task_name_list.split('|')):
                        ret = core_obj.del_group(group_name, task_name)
                        for line in ret:
                            return_message.append(line)
                        try:
                            main_p.group_conn.rmv(group_name, task_name)
                        except Exception, e:
                            return_message.append("NOK : Exception in set group del [%s]" % str(e))
                else:
                    if group_name not in core_obj.all_group: raise Exception, '[%s] gruop not exists' % group_name
                    for task_name in core_obj.all_group[group_name]:
                        ret = core_obj.del_group(group_name, task_name)
                        for line in ret:
                            return_message.append(line)
                        try:
                            main_p.group_conn.rmv(group_name, task_name)
                        except Exception, e:
                            return_message.append("NOK : Exception in set group del [%s]" % str(e))
                        
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Excetpion occured in del group [%s]" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json([error_msg])
        

