import json
import EventFlow.MessageFormatter as MF

def shw_global_queue(main_p, command_data, web=False):
    try:
        return_value = []
        for x in main_p.mon_deque:
            return_value.append( '[%s] : %s : %s' % x )
        if not web:
            return MF.make_message(return_value)
        else:
            return MF.simple_result_json( return_value, header='GLOBAL_QUEUE', column = [ 'DATETIME', 'DIRECTION', 'MESSAGE' ] )
    except Exception, e:
        error_msg = "NOK : Exception occured in shw global_queue [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def del_task_queue(main_p, command_data, web=False):
    try:
        return_value = []
        command_string = ' '.join(command_data[2:])
        if len(command_string.strip()) == 0: command_string = 'all'

        for task_name in map(lambda x:x.strip(), command_string.split(',')):
            if task_name not in main_p.thread_daemon_list['Core'].all_task_object:
                if task_name.lower() == 'all':
                    for _task_name in main_p.thread_daemon_list['Core'].all_task_object:
                        try: 
                            for line in main_p.thread_daemon_list['Core'].all_task_object[_task_name].clear_queue():
                                return_value.append(line)
                        except Exception, e:
                            return_value.append( "NOK : Exception occured in clear queue [%s]" % str(e) )
                elif task_name in main_p.thread_daemon_list['Core'].all_group:
                    for _task_name in main_p.thread_daemon_list['Core'].all_group[task_name]:
                        try: 
                            for line in main_p.thread_daemon_list['Core'].all_task_object[_task_name].clear_queue():
                                return_value.append(line)
                        except Exception, e:
                            return_value.append( "NOK : Exception occured in clear queue [%s]" % str(e) )
                else:
                    return_value.append( "NOK : [%s] task not exists" % task_name )
            else:
                for line in main_p.thread_daemon_list['Core'].all_task_object[task_name].clear_queue():
                    return_value.append(line)
        if not web:
            return MF.make_message( return_value )
        else:
            return MF.simple_result_json( return_value )
    except Exception, e:
        error_msg = "NOK : Exception occured in del task queue : %s" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json( [error_msg] )

def sav_task_queue(main_p, command_data, web=False):
    tasks = main_p.thread_daemon_list['Core'].all_task_object
    command_string = ' '.join(command_data[1:])
    result_message = []
    try:
        if command_string.strip() == '': command_string = 'all'
        task_list = map(lambda x:x.strip(), command_string.split(','))
        if 'all' in task_list: 
            for task_name in tasks.keys():
                if task_name not in task_list: task_list.append(task_name)

        for task_name in task_list:
            if task_name not in tasks:
                result_message.append('NOK : [%s] task not exist')
                continue
            ret = tasks[task_name].save_queue()
            for line in ret:
                result_message.append(line)
        if not web: return MF.make_message( result_message )
        else: return MF.simple_result_json( result_message )
    except Exception, e:
        error_msg = "NOK : Exception occured in del task queue : %s" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json( [error_msg] )

def lad_task_queue(main_p, command_data, web=False):
    tasks = main_p.thread_daemon_list['Core'].all_task_object
    command_string = ' '.join(command_data[1:])
    result_message = []
    try:
        if command_string.strip() == '': command_string = 'all'
        task_list = map(lambda x:x.strip(), command_string.split(','))
        if 'all' in task_list: 
            for task_name in tasks.keys():
                if task_name not in task_list: task_list.append(task_name)

        for task_name in task_list:
            if task_name not in tasks:
                result_message.append('NOK : [%s] task not exist')
                continue
            ret = tasks[task_name].load_queue()
            for line in ret:
                result_message.append(line)
        if not web: return MF.make_message( result_message )
        else: return MF.simple_result_json( result_message )
    except Exception, e:
        error_msg = "NOK : Exception occured in del task queue : %s" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json( [error_msg] )
