import json, importlib
import EventFlow.MessageFormatter as MF
from EventFlow.Interface.OptParserForTask import OptParserForTask as OptionParser
from EventFlow.Interface.OptParserForTask import OptionParsingError

def shw_ready(main_p, command_data, web=False):
    return_message = []
    task_list_obj = main_p.thread_daemon_list['Core'].all_task_object
    add_list_obj = main_p.thread_daemon_list['Core'].add_list
    command_string = ' '.join(command_data[2:])
    for task_name in map(lambda x:x.strip(), command_string.split(',')):
        if task_name in task_list_obj:
            return_message.append("OK : [%s] task ready" % task_name)
            continue
        message_data = "NOK : [%s] task not exists" % task_name
        for item in add_list_obj:
            if item[1] == task_name: message_data = "OK : [%s] task not ready" % task_name
        return_message.append(message_data)
    if not web: return MF.make_message(return_message)
    else: return MF.simple_result_json(return_message)

def shw_status(main_p, command_data, web=False, recursive=False):
    task_list_obj = main_p.thread_daemon_list['Core'].all_task_object
    group_list_obj = main_p.thread_daemon_list['Core'].all_group
    try:
        return_hash = {}
        return_hash['STATUS'] = []
        if recursive:
            command_string = command_data
        else:
            command_string = ' '.join(command_data[2:])

        if type(command_string) == type('') and len(command_string.strip()) == 0: command_string = 'all'

        for command in map(lambda x:x.strip(), command_string.split(',')):
            if command not in task_list_obj:
                if command.lower() == 'all':
                    for _task_name in task_list_obj.keys():
                        ret = shw_status(main_p, _task_name, recursive=True)
                        for _key in ret['STATUS']:
                            return_hash['STATUS'].append(_key)
                elif command in group_list_obj:
                    for _task_name in group_list_obj[command]:
                        ret = shw_status(main_p, _task_name, recursive=True)
                        for _key in ret['STATUS']:
                            return_hash['STATUS'].append(_key)
                else:
                    temp_hash = {}
                    temp_hash['name'] = command
                    temp_hash['error'] = 'NOK : [%s] task not exists' % command
                    return_hash['STATUS'].append(temp_hash)
            else:
                return_hash['STATUS'].append(task_list_obj[command].status)
        if recursive:
            return return_hash
        if not web:
            return_message = []
            prefix = '%10s | %86s'
            return_hash['STATUS'] = sorted(return_hash['STATUS'], key=lambda value:value['name'])
            for _item in return_hash['STATUS']:
                return_message.append('=' * 100)
                return_message.append(_item['name'])
                return_message.append('-' * 100)
                if 'error' in _item:
                    return_message.append( prefix % ('error', _item['error']) )
                    continue
                for _key in [ 'type', 'status', 'act-status', 'act-time', 'act-count', 'pid', 'command' ]:
                    return_message.append( prefix % ( _key, str(_item[_key]) ))
                return_message.append('-' * 100)
                return_message.append('last-status')
                return_message.append('-' * 100)
                for _key in [ 'std-in', 'std-out', 'std-err' ]:
                    return_message.append( prefix % ( _key, str(_item['last-status']['last-' + _key]) ) )
            return MF.make_message(return_message)
        else:
            return MF.make_json(return_hash)
    except Exception, e:
        error_msg = "NOK : Exception occured in shw status [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def act_task(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[1:])
        for task_name in map(lambda x:x.strip(), command_string.split(',')):
            ret = main_p.thread_daemon_list['Core'].act_task(task_name)
            for line in ret:
                return_message.append(line)
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in act task [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def trm_task(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[1:])
        for task_name in map(lambda x:x.strip(), command_string.split(',')):
            ret = main_p.thread_daemon_list['Core'].trm_task(task_name)
            for line in ret:
                return_message.append(line)
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in trm task [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def shw_recovery(main_p, command_data, web=False):
    result_list = []
    for item in main_p.thread_daemon_list['Core'].recovery_result:
        result_list.append( (item, main_p.thread_daemon_list['Core'].recovery_result[item][0], main_p.thread_daemon_list['Core'].recovery_result[item][1] ) )
    if not web: return MF.shw_recovery_list(result_list)
    else: return MF.simple_result_json(result_list, header='RECOVERY', column=['NAME', 'START_TIME', 'END_TIME'])

def shw_task(main_p, command_data, web=False):
    try:
        parser = OptionParser()
        parser.add_option('-t', '--task', dest='task')
        parser.add_option('-y', '--task-type', dest='task_type')
        parser.add_option('-s', '--status', dest='status')
        parser.add_option('-a', '--act-status', dest='act_status')
        parser.add_option('-p', '--pid', dest='pid')
        options, _ = parser.parse_args(command_data)
    except OptionParsingError, e:
        error_msg = 'NOK : shw task option error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    try:
        if options.task: options.task = map(lambda x:x.strip(), options.task.split(','))
        if options.task_type: options.task_type = map(lambda x:x.strip(), options.task_type.split(','))
        if options.status: options.status = map(lambda x:x.strip(), options.status.split(','))
        if options.act_status: options.act_status = map(lambda x:x.strip(), options.act_status.split(','))
        if options.pid: options.pid = map(lambda x:x.strip(), options.pid.split(','))
    except Exception, e:
        error_msg = 'NOK : shw task option split error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    def view_filter(options, data, message):
        if options.task != None and data[1] not in options.task: return message
        if options.task_type != None and data[0] not in options.task_type: return message
        if options.status != None and data[2] not in options.status: return message
        if options.act_status != None and data[3] not in options.act_status: return message
        if options.pid != None and data[6] not in options.pid: return message
        message.append(data)
        return message

    try:
        task_name_list = main_p.thread_daemon_list['Core'].all_task_object.keys()
        result_list = []
        for task_name in task_name_list:
            pso = main_p.thread_daemon_list['Core'].all_task_object[task_name].status
            result_list = view_filter( options,  (pso['type'], pso['name'], pso['status'], pso['act-status'], pso['act-count'], pso['act-time'], pso['pid']), result_list)
        if not web: return MF.shw_task_list(result_list)
        else: return MF.simple_result_json(result_list, header='TASKS', column=[ 'TYPE', 'NAME', 'STATUS', 'ACT-STATUS', 'ACT-COUNT', 'ACT-TIME', 'PID' ])
    except Exception, e:
        error_msg = "NOK : Exception occured in shw task [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def set_recovery(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = " ".join(command_data[2:])
        for command in map(lambda x:x.strip(), command_string.split(',')):
            _task_name, _message = map(lambda x:x.strip(), command.split(':'))
            ret = main_p.thread_daemon_list['Core'].add_recovery(_task_name, _message)
            for line in ret:
                return_message.append(line)
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in set recovery [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])


def set_task(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = " ".join(command_data[2:])
        for command in map(lambda x:x.strip(), command_string.split(',')):
            try: _type, _name, _command, _file_name, _enc_data = command.split(':')
            except:
                try: _type, _name, _command = command.split(':')
                except Exception, e:
                    return_message.append("NOK : Exception occured in set task : %s" % str(e))
                    continue
                _file_name = None
                _enc_data = None

            helper_module = importlib.import_module('EventFlow.Task.' + _type[0].upper() + _type[1:].lower() + 'Task')
            helper_class = getattr(helper_module, _type[0].upper() + _type[1:].lower() + 'TaskHelper')(main_p, _name, _command, _file_name, _enc_data)
            _command = helper_class.run()
            ret = main_p.thread_daemon_list['Core'].add_task(_type.lower(), _name, _command)
            for line in ret:
                return_message.append(line)
            try:
                main_p.node_conn.set(_type.lower(), _name, _command)
            except Exception, e:
                return_message.append("NOK : Exception occured in set task save : %s" % str(e))
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in set task [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def del_task(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        for task_name in map(lambda x:x.strip(), command_string.split(',')):
            ret = main_p.thread_daemon_list['Core'].del_task(task_name)
            for line in ret:
                return_message.append(line)
            try:
                main_p.node_conn.rmv(task_name)
            except Exception, e:
                return_message.append( 'NOK : Exception occured in del task db : %s' % str(e))
        if not web:
            return MF.make_message(return_message)
        else:
            return_data = {}
            return_data['RESULTS'] = []
            for message in return_message:
                result, msg = map(lambda x:x.strip(), message.strip().split(':', 1))
                temp_hash = {}
                temp_hash['RESULT'] = result
                temp_hash['MESSAGE'] = msg
                return_data['RESULTS'].append(temp_hash)
            return MF.make_json(return_data)
    except Exception, e:
        if not web:
            return MF.make_message( "NOK : Exception occured in del task : %s" % str(e) )
        else:
            return MF.make_json( { "RESULT" : "NOK", "MESSAGE" : " Exception occured in del task : %s" % str(e) } )

