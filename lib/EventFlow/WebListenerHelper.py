

def _call_config_interface(method, json_data, etc_data):
    if method == 'GET':
        default_command = 'shw conf'
        if json_data:
            if 'CHANGEABLE' in json_data:
                if json_data['CHANGEABLE'].upper() == 'TRUE': default_command += ' -c'
                if json_data['CHANGEABLE'].upper() == 'FALSE': default_command += ' -n'
            if 'KEY' in json_data:
                default_command += ' -k %s' % json_data['KEY']
        return default_command
    elif method == 'PUT':
        default_command = 'set conf'
        if not json_data: raise Exception, 'PUT method needs json data'
        for item in json_data['CONFIGS']:
            if default_command != 'set conf': default_command += ','
            default_command += ' %s:%s' % (item['KEY'], str(item['VALUE']))
        return default_command
    else: raise Exception, 'not supported method [%s]' % method

def _call_tasks_interface(method, json_data, etc_data):
    if method == 'GET':
        default_command = 'shw task'
        if json_data:
            if 'TASK' in json_data: default_command += ' -t %s' % json_data['TASK']
            if 'TYPE' in json_data: default_command += ' -y %s' % json_data['TYPE']
            if 'STATUS' in json_data: default_command += ' -s %s' % json_data['STATUS']
            if 'ACT-STATUS' in json_data: default_command += ' -a %s' % json_data['ACT-STATUS']
            if 'PID' in json_data: default_command += ' -p %s' % json_data['PID']
        return default_command
    elif method == 'POST':
        default_command = 'set task'
        if not json_data: raise Exception, 'POST method needs json data'
        for item in json_data['TASKS']:
            if default_command != 'set task': default_command += ','
            if len(item.keys()) == 3:
                default_command += ' %s:%s:%s' % (item['TYPE'], item['NAME'], item['COMMAND'])
            elif len(item.keys()) == 5:
                default_command += ' %s:%s:%s:%s:%s' % (item['TYPE'], item['NAME'], item['COMMAND'], item['FILE_NAME'], item['ENC_DATA'])
            else:
                raise Exception, "POST method key does not matched"
        return default_command
    else: raise Exception, 'not supported method [%s]' % method


def _call_groups_interface(method, json_data, etc_data):
    if method == 'GET':
        default_command = 'shw group'
        if json_data:
            if 'GROUP' in json_data: default_command + ' -g %s' % json_data['GROUP']
            if 'TASK' in json_data: default_command + ' -t %s' % json_data['TASK']
        return default_command
    elif method == 'POST':
        default_command = 'set group'
        if not json_data: raise Exception, 'POST method needs json data'
        for item in json_data['GROUPS']:
            if default_command != 'set group': default_command += ','
            if len(item.keys()) == 2:
                default_command += ' %s:%s' % (item['GROUP'], '|'.join(map(lambda x:x.strip(), item['TASK'].strip().split(','))))
        return default_command
    elif method == 'PUT':
        if not json_data:raise Exception, 'PUT method needs json data'
        return json_data['STATUS'] + ' ' + json_data['GROUP']
    elif method == 'DELETE':
        default_command = 'del group'
        if not json_data:raise Exception, 'DELETE method needs json data'
        for item in json_data['GROUPS']:
            if default_command != 'del group': default_command += ','
            if len(item.keys()) == 1:
                default_command += ' %s' % item['GROUP']
            elif len(item.keys()) == 2:
                default_command += ' %s:%s' % (item['GROUP'], '|'.join(map(lambda x:x.strip(), item['TASK'].strip().split(','))))
        return default_command
    else: raise Exception, 'not supported method [%s]' % method

def _call_schedules_interface(method, json_data, etc_data):
    if method == 'GET':
        default_command = 'shw schedule'
        if json_data:
            if 'TIME_FORMAT' in json_data: default_command += ' -t %s' % json_data['TIME_FORMAT']
            if 'TASK' in json_data: default_command += ' -t %s' % json_data['TASK']
        return default_command
    elif method == 'POST':
        default_command = 'set schedule'
        if not json_data:raise Exception, 'POST method needs json data'
        for item in json_data['SCHEDULES']:
            if default_command != 'set schedule': default_command += ','
            if len(item.keys()) == 3:
                default_command += ' %s:%s:%s' % ( item['TIME_FORMAT'], item['TASK'], item['MESSAGE'] )
        return default_command
    elif method == 'DELETE':
        default_command = 'del schedule'
        if not json_data:raise Exception, 'DELETE method needs json data'
        for item in json_data['SCHEDULES']:
            if default_command != 'del schedule': default_command += ',' 
            if len(item.keys()) == 2:
                default_command += ' %s:%s' % ( item['TIME_FORMAT'], item['TASK'] )
        return default_command
    else: raise Exception, 'not supported method [%s]' % method


def _call_flows_interface(method, json_data, etc_data):
    if method == 'GET':
        default_command = 'shw flow'
        if json_data:
            if 'TASK' in json_data: default_command += ' -t %s' % json_data['TASK']
            if 'TYPE' in json_data: default_command += ' -f %s' % json_data['TYPE']
        return default_command
    elif method == 'POST':
        default_command = 'set flow'
        if not json_data: raise Exception, 'POST method needs json data'
        for item in json_data['FLOWS']:
            if default_command != 'set flow': default_command += ','
            if len(item.keys()) == 3:
                default_command += ' %s:%s:%s' % ( item['FLOW_TYPE'], 
                                                    '|'.join(item['FLOW_FROM'].strip().split(',')),
                                                    '|'.join(item['FLOW_TO'].strip().split(',')) )
        return default_command
    elif method == 'DELETE':
        default_command = 'del flow'
        if not json_data: raise Exception, 'DELETE method needs json data'
        for item in json_data['FLOWS']:
            if default_command != 'set flow': default_command += ','
            if len(item.keys()) == 3:
                default_command += ' %s:%s:%s' % ( item['FLOW_TYPE'], 
                                                    '|'.join(item['FLOW_FROM'].strip().split(',')),
                                                    '|'.join(item['FLOW_TO'].strip().split(',')) )
        return default_command
    else: raise Exception, 'not supported method [%s]' % method


def _call_task_interface(method, json_data, etc_data):
    task_name = etc_data['task_name']
    if method == 'GET':
        return 'shw task -t %s' % task_name
    elif method == 'DELETE':
        return 'del task %s' % task_name
    else: raise Exception, 'not supported method [%s]' % method


def _call_queue_interface(method, json_data, etc_data):
    task_name = etc_data['task_name']
    if method == 'DELETE':
        return 'del task_queue %s' % task_name
    else: raise Exception, 'not supported method [%s]' % method
        

def _call_stdin_interface(method, json_data, etc_data):
    task_name = etc_data['task_name']
    if method == 'GET':
        return 'shw stdin %s' % task_name
    elif method == 'PUT':
        if not json_data: raise Exception, 'PUT method needs json data'
        return 'set stdin %s:%s' % (task_name, json_data['MESSAGE'])
    else: raise Exception, 'not supported method [%s]' % method

def _call_global_queue_interface(method, json_data, etc_data):
    if method == 'GET':
        return 'shw global_queue'
    else: raise Exception, 'not supported method [%s]' % method

def _call_status_interface(method, json_data, etc_data):
    task_name = etc_data['task_name']
    if method == 'GET':
        return 'shw status %s' % task_name
    elif method == 'PUT':
        if not json_data: raise Exception, 'PUT method needs json data'
        return '%s %s' % (json_data['STATUS'], task_name)
    else: raise Exception, 'not supported method [%s]' % method

def _call_recovery_interface(method, json_data, etc_data):
    if method == 'GET':
        return 'shw recovery'
    elif method == 'POST':
        if not json_data: raise Exception, 'POST method needs json data'
        default_command = 'set recovery'
        for item in json_data['RECOVERY']:
            if default_command != 'set recovery': default_command += ','
            default_command += ' %s:%s' % (item['TASK'], item['MESSAGE'])
        return default_command
    else: raise Exception, 'not supported method [%s]' % method



def _call_ready_interface(method, json_data, etc_data):
    task_name = etc_data['task_name']
    if method == 'GET':
        return 'shw ready %s' % task_name
    else: raise Exception, 'not supported method [%s]' % method
    


    

_default_config = {}
_default_config['configs'] = _call_config_interface
_default_config['tasks'] = _call_tasks_interface
_default_config['groups'] = _call_groups_interface
_default_config['schedules'] = _call_schedules_interface
_default_config['flows'] = _call_flows_interface
_default_config['task'] = _call_task_interface
_default_config['queue'] = _call_queue_interface
_default_config['stdin'] = _call_stdin_interface
_default_config['global_queue'] = _call_global_queue_interface
_default_config['status'] = _call_status_interface
_default_config['recovery'] = _call_recovery_interface
_default_config['ready'] = _call_ready_interface

