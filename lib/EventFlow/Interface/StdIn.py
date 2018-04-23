import json
import EventFlow.MessageFormatter as MF

def set_stdin(main_p, command_data, web=False):
    return_message = []
    command_string = ' '.join(command_data[2:])
    for command in map(lambda x:x.strip(), command_string.split(',')):
        dst_task, message = command.split(':')
        if dst_task not in main_p.thread_daemon_list['Core'].all_task_object:
            return_message.append("NOK : [%s] task not exists" % dst_task)
            continue
        main_p.thread_daemon_list['Core'].all_task_object[dst_task].put_queue(message)
        return_message.append("OK : set stdin [%s] to %s" % (message, dst_task))
    if not web: return MF.make_message(return_message)
    else: return MF.simple_result_json(return_message)

def shw_stdin(main_p, command_data, web=False, recursive=False):
    core_obj = main_p.thread_daemon_list['Core']
    if recursive:
        command_string = command_data
    else:
        command_string = ' '.join(command_data[2:])
    if command_string.strip() == '': command_string = 'all'
    result_hash = {}
    result_hash['QUEUES'] = []
    for task_name in map(lambda x:x.strip(), command_string.split(',')):
        if task_name not in core_obj.all_task_object:
            if task_name == 'all':
                for sub_task_name in core_obj.all_task_object:
                    sub_return_message = shw_stdin(main_p, sub_task_name, recursive=True)
                    for item in sub_return_message['QUEUES']:
                        result_hash['QUEUES'].append(item)
            else:
                temp_hash = {}
                temp_hash['NAME'] = task_name
                temp_hash['ERROR'] = []
                temp_hash['BROADCASTING STDIN'] = []
                temp_hash['SHARING STDIN'] = []
                temp_hash['ERROR'].append('NOK : task not exists')
                result_hash['QUEUES'].append(temp_hash)
        else:
            temp_hash = {}
            temp_hash['NAME'] = task_name
            temp_hash['ERROR'] = []
            temp_hash['BROADCASTING STDIN'] = []
            for msg in core_obj.all_task_object[task_name].broadcast_deq.__copy__():
                temp_hash['BROADCASTING STDIN'].append(msg)
            temp_hash['SHARING STDIN'] = []
            for dst_task in core_obj.all_task_object[task_name].sharing_task_list:
                for msg in dst_task.sharing_deq.__copy__():
                    temp_hash['SHARING STDIN'].append(msg)
            result_hash['QUEUES'].append(temp_hash)
    if recursive:
        return result_hash
    if not web:
        temp_list = result_hash['QUEUES'][:]
        sorted(temp_list, key=lambda queue_data: queue_data['NAME'])
        result_message = []
        for item in temp_list:
            result_message.append( '=' * 100)
            result_message.append( item['NAME'] )
            result_message.append( '-' * 100)
            for _key in item:
                if _key == 'NAME': continue
                if len(item[_key]) == 0: continue
                result_message.append(_key)
                result_message.append( '-' * 100)
                for line in item[_key]:
                    result_message.append( '  ' + line )
        return MF.make_message(result_message)
    else:
        return MF.make_json(result_hash)
        

