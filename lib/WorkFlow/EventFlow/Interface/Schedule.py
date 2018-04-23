import json
import EventFlow.MessageFormatter as MF
from EventFlow.Interface.OptParserForTask import OptParserForTask as OptionParser
from EventFlow.Interface.OptParserForTask import OptionParsingError

def set_schedule(main_p, command_data, web=False):
    core_obj = main_p.thread_daemon_list['Core']
    command_string = ' '.join(command_data[2:])
    try:
        for command in map(lambda x:x.strip(), command_string.split(',')):
            time_info, dst_task, message = map(lambda x:x.strip(), command_string.split(':'))
            if len(time_info.split()) != 5: raise Exception, 'time format follow cron expression'
            if dst_task not in core_obj.all_task_object: raise Exception, '[%s] task not exists' % dst_task
            main_p.schedule_conn.set(time_info, dst_task, message)
    except Exception, e:
        error_msg = 'NOK : Exception occured in set schedule [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
    return_msg = "OK : schedule set success"
    if not web: return MF.make_message(return_msg)
    else: return MF.simple_result_json([return_msg])

def del_schedule(main_p, command_data, web=False):
    command_string = ' '.join(command_data[2:])
    try:
        for command in map(lambda x:x.strip(), command_string.split(',')):
            time_info, dst_task = map(lambda x:x.strip(), command_string.split(':'))
            if len(time_info.split()) != 5: raise Exception, "time format follow cron expression"
            main_p.schedule_conn.rmv(time_info, dst_task)
    except Exception, e:
        error_msg = 'NOK : Exception occured in del schedule [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
    return_msg = "OK : schedule del success"
    if not web: return MF.make_message(return_msg)
    else: return MF.simple_result_json([return_msg])

def shw_schedule(main_p, command_data, web=False):
    try:
        parser = OptionParser()
        parser.add_option('-f', '--time-format', dest='time_format')
        parser.add_option('-t', '--task', dest='task')
        options, _ = parser.parse_args(command_data)
    except OptionParsingError, e:
        error_msg = 'NOK : shw schedule option error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
    try:
        if options.time_format != None:
            temp_string_list = []
            start = False
            for single_item in command_data[2:]:
                if single_item.lower() in [ '-f', '--time-format' ]:
                    start = True
                    continue

                if start:
                    if single_item.startswith('-'): break
                    temp_string_list.append(single_item)

            options.time_format = ' '.join(temp_string_list)
    except Exception, e:
        error_msg = 'NOK : shw schedule option time format make failed [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    def view_check(options, data, message):
        if options.time_format != None and data[0] not in options.time_format: return message
        if options.task != None and data[1] not in options.task: return message
        message.append( data )
        return message

    try:
        return_value = []
        for schedule_info in main_p.schedule_conn.lst():
            return_value = view_check(options, schedule_info, return_value)
        if not web: return MF.shw_schedule_list(return_value)
        else: return MF.simple_result_json(return_value, header='SCHEDULES', column = [ 'TIME_FORMAT', 'TASK', 'MESSAGE' ] )
    except Exception, e:
        error_msg = 'NOK : Exception occured in shw schedule [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
