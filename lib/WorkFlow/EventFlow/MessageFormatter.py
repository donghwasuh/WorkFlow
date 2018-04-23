import json

def create_begin_end(message):
    return "<begin>\n%s\n<end>\n" % message.strip()

def join_all_message(messages):
    return_value = []
    for item in messages:
        if item[-1] != '\n': return_value.append( item + '\n' )
        else: return_value.append(item)
    return ''.join(return_value)


def make_message(message):
    if type(message) in [ type([]), type(()) ]:
        return create_begin_end(join_all_message(message))
    else:
        return create_begin_end(str(message))

def dict_upper(dict_data):
    if type(dict_data) == type({}):
        temp_dict = {}
        for _key in dict_data.keys():
            temp_dict[_key.upper()] = dict_upper(dict_data[_key])
        return temp_dict
    elif type(dict_data) == type([]):
        temp_dict = []
        for item in dict_data:
            temp_dict.append(dict_upper(item))
        return temp_dict
    else:
        return dict_data

def make_json(dict_data):
    return json.dumps(dict_upper(dict_data), indent=4)


def simple_result_json(message_list, header='RESULTS', column=[ 'RESULT', 'MESSAGE' ]):
    result_hash = {}
    result_hash[header] = []

    for line in message_list:
        if type(line) == type('') or type(line) == type(u''):
            line_data = map(lambda x:x.strip(), line.split(':'))
        else:
            line_data = line
        temp_hash = {}
        for i in range(len(column)):
            temp_hash[column[i]] = line_data[i]
        result_hash[header].append(temp_hash)

    return make_json(result_hash)
            
def front_end_maker():
    return "=" * 100

def middle_maker():
    return "-" * 100

def shw_task_list(process_data):
    prefix = "%10s | %16s | %10s | %10s | %10s | %15s | %10s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'type', 'process task', 'status', 'act status', 'act count', 'act time', 'pid' ) )
    ml.append(middle_maker())
    for item in process_data:
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)

def shw_conf_list(config_data):
    prefix = "%30s | %53s | %10s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'config_key', 'config_value', 'changeable' ) )
    ml.append(middle_maker())
    for item in config_data:
        if type(item[1]) == type('') and len(item[1]) > 53:
            item = ( item[0], '...' + item[1][len(item[1]) - 50:], item[2] )
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)

def shw_flow_list(flow_data):
    prefix = "%10s | %41s | %42s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'flow type', 'flow from', 'flow to' ) )
    ml.append(middle_maker())
    for item in flow_data:
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)
  
def shw_group_list(group_data):
    prefix = "%18s | %78s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'group name', 'task list' ) )
    ml.append(middle_maker())
    for item in group_data:
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)

def shw_schedule_list(schedule_data):
    prefix = "%13s | %20s | %60s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'time info', 'dst node', 'message' ) )
    ml.append(middle_maker())
    for item in schedule_data:
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)

def shw_recovery_list(recovery_data):
    prefix = "%63s | %15s | %15s"
    ml = []
    ml.append(front_end_maker())
    ml.append( prefix % ( 'recover task name', 'start time', 'end time' ) )
    ml.append(middle_maker())
    for item in recovery_data:
        ml.append( prefix % item )
    ml.append(front_end_maker())
    return make_message(ml)
    

if __name__ == '__main__':
    print shw_conf_list([])
    
    













