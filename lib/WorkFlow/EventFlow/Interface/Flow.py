import json
import EventFlow.MessageFormatter as MF
from EventFlow.Interface.OptParserForTask import OptParserForTask as OptionParser
from EventFlow.Interface.OptParserForTask import OptionParsingError

def shw_flow(main_p, command_data, web=False):
    try:
        parser = OptionParser()
        parser.add_option('-f', '--flow-type', dest='flow_type')
        parser.add_option('-t', '--task', dest='task')
        options, _ = parser.parse_args(command_data)
    except OptionParsingError, e:
        error_msg = 'NOK : shw flow option error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    try:
        if options.flow_type != None:
            options.flow_type = map(lambda x:x.strip(), options.flow_type.strip().split(','))
        if options.task != None:
            options.task = map(lambda x:x.strip(), options.task.strip().split(','))
    except Exception, e:
        error_msg = 'NOK : shw flow option split error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    def view_check(options, data, message):
        if options.flow_type != None:
            if data[0] not in options.flow_type: return message

        if options.task != None:
            if data[1] not in options.task:
                add_check = False
                for item in data[2]:
                    if item in options.task: add_check = True
                if not add_check: return message
        message.append(data)
        return message
                

    try:
        result_message = []
        core_obj = main_p.thread_daemon_list['Core']

        for from_task in core_obj.all_broad_flow:
            result_message = view_check(options, ( 'broad', from_task, core_obj.all_broad_flow[from_task] ), result_message)
        for from_task in core_obj.all_share_flow:
            result_message = view_check(options, ( 'share', from_task, core_obj.all_share_flow[from_task] ), result_message)

        if not web:
            return MF.shw_flow_list(result_message) 
        else:
            return_hash = {}
            return_hash['FLOWS'] = {}
            for item in result_message:
                if item[0] not in return_hash['FLOW']: return_hash['FLOW'][item[0]] = []
                temp_hash = {}
                temp_hash['FROM'] = item[1]
                temp_hash['TO'] = item[2]
                return_hash['FLOW'][item[0]].append(temp_hash)
            return MF.make_json( return_hash )

    except Exception, e:
        error_msg = "NOK : Exception occured in shw flow [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def set_flow(main_p, command_data, web=False):
    core_obj = main_p.thread_daemon_list['Core']
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        for command in map(lambda x:x.strip(), command_string.split(',')):
            flow_type, flow_from, flow_to = map(lambda x:x.strip(), command.split(':'))
            for flow_from_item in map(lambda x:x.strip(), flow_from.split('|')):
                for flow_to_item in map(lambda x:x.strip(), flow_to.split('|')):
                    ret = core_obj.add_flow(flow_type.lower(), flow_from_item, flow_to_item)
                    for item in ret:
                        return_message.append(item)
                    try: main_p.flow_conn.set(flow_type.lower(), flow_from_item, flow_to_item)
                    except Exception, e: return_message.append( 'NOK : Exception occured in set flow save : %s' % str(e) )
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in set flow [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

def del_flow(main_p, command_data, web=False):
    core_obj = main_p.thread_daemon_list['Core']
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        for command in map(lambda x:x.strip(), command_string.split(',')):
            flow_type, flow_from, flow_to = map(lambda x:x.strip(), command.split(':'))
            for flow_from_item in map(lambda x:x.strip(), flow_from.split('|')):
                for flow_to_item in map(lambda x:x.strip(), flow_to.split('|')):
                    ret = core_obj.del_flow(flow_type.lower(), flow_from_item, flow_to_item)
                    for item in ret:
                        return_message.append(item)
                    try: main_p.flow_conn.rmv(flow_type.lower(), flow_from_item, flow_to_item)
                    except Exception, e: return_message.append( 'NOK : Exception occured in rmv flow db : %s' % str(e) )
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in del flow [%s]" % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
    
            
