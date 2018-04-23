import json

import EventFlow.MessageFormatter as MF
from EventFlow.Interface.OptParserForTask import OptParserForTask as OptionParser
from EventFlow.Interface.OptParserForTask import OptionParsingError

def shw_conf(main_p, command_data, web=False):

    # parser init ( this parser modified for not exit
    try:
        parser = OptionParser()
        parser.add_option('-n', '--not-changeable', dest='not_changeable', default=False, action='store_true')
        parser.add_option('-c', '--changeable', dest='changeable', default=False, action='store_true')
        parser.add_option('-k', '--key', dest='config_key')
        options, _ = parser.parse_args(command_data)
    except OptionParsingError, e:
        error_msg = 'NOK : shw conf option error [%s]' % str(e)
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])

    # special value which value contains spaace
    if options.config_key:
        temp_command = []
        for command in command_data:
            if command.startswith('-') and command not in ['-k', '--key']:continue
            temp_command.append(command)
        # if option, -k event flow home, dump dir
        if '-k' in temp_command:
            string_data = ' '.join(temp_command).strip().split('-k')[1].strip()
        else:
            string_data = ' '.join(temp_command).strip().split('--key')[1].strip()
        options.config_key = map(lambda x:x.strip(), string_data.split(","))

    # add checker
    def view_checker(options, data, message):
        if options.config_key != None and data[0] not in options.config_key: return message
        if data[2] == 'Y':
            if not ( not options.not_changeable and not options.changeable ) and not options.changeable: return message
        else:
            if not ( not options.not_changeable and not options.changeable ) and not options.not_changeable: return message
        message.append(data)
        return message

    try:
        main_p.config_reload()
        result_message = []
        result_message = view_checker( options, ("event flow home", main_p.home_path, "N"), result_message)
        result_message = view_checker( options, ("console connect address", main_p.host, "N"), result_message)
        result_message = view_checker( options, ("console connect port", main_p.port, "N") , result_message)
        result_message = view_checker( options, ("dump dir", main_p.home_path + "/dmp/" + main_p.name, "N"), result_message )
        result_message = view_checker( options, ("max cmd queue size", main_p.max_cmd_queue_size, "Y"), result_message )
        result_message = view_checker( options, ("max monitoring deque size", main_p.max_mon_deque_size, "Y"), result_message )
        result_message = view_checker( options, ("max save deque size", main_p.max_save_deque_size, "Y"), result_message )
        result_message = view_checker( options, ("error data file skip", main_p.error_data_file_skip, "Y"), result_message )
        result_message = view_checker( options, ("kill wait time", main_p.kill_wait_time, "Y"), result_message )
        result_message = view_checker( options, ("event save file", main_p.save_event_file_path, "Y"), result_message )
        result_message = view_checker( options, ("scheduler run", main_p.scheduler_run, "Y"), result_message )
        result_message = view_checker( options, ("flask run", main_p.flask_run, "Y"), result_message )
        result_message = view_checker( options, ("flask port", main_p.flask_port, "Y"), result_message )
        result_message = view_checker( options, ("flask shutdown code", main_p.flask_shutdown_code, "N"), result_message )
        result_message = view_checker( options, ("resource monitor size", main_p.resource_monitor_size, "Y"), result_message )
        result_message = view_checker( options, ("result monitor size", main_p.result_monitor_size, "Y"), result_message )
        result_message = view_checker( options, ("announcer run", main_p.announcer_run, "Y"), result_message )
        result_message = view_checker( options, ("announcer dst address", main_p.announcer_dst_addr, "Y"), result_message )
        result_message = view_checker( options, ("announcer dst port", main_p.announcer_dst_port, "Y"), result_message )
        result_message = view_checker( options, ('announcer result api', main_p.announcer_result_api, 'Y'), result_message )
        result_message = view_checker( options, ('announcer resource api', main_p.announcer_resource_api, 'Y'), result_message )
        result_message = view_checker( options, ('announcer alert api', main_p.announcer_alert_api, 'Y'), result_message )
        result_message = view_checker( options, ('recovery time out', main_p.recovery_time_out, 'Y'), result_message )
        result_message = view_checker( options, ('recovery delete time', main_p.recovery_del_time, 'Y'), result_message )
        result_message = view_checker( options, ('work directory', main_p.work_directory, 'Y'), result_message )
        if not web:
            return MF.shw_conf_list(result_message) 
        else:
            return MF.simple_result_json(result_message, header='CONFIGS', column=['KEY', 'VALUE', 'CHANGEABLE'])
    except Exception, e:
        error_msg = "NOK : Exception occured in shw conf [%s]" % str(e)
        if not web: return MF.make_message( error_msg )
        else: return MF.simple_result_json( [ error_msg ] )

def set_conf(main_p, command_data, web=False):
    try:
        return_message = []
        command_string = ' '.join(command_data[2:])
        for set_data in map( lambda x:x.strip(), command_string.split(",") ):
            _key, _value = set_data.split(":")
            _key = _key.strip()
            _value = _value.strip()
            if _key not in [ 'event flow home', 'console connect address', 'console connect port',
                                'dump dir', 'max cmd queue size', 'max monitoring deque size',
                                'max save deque size', 'error data file skip', 'kill wait time',
                                'event save file', 'scheduler run', 'flask run', 'flask port',
                                'flask shutdown code', 'result monitor size', 'resource monitor size',
                                'announcer run', 'announcer dst address', 'announcer dst port',
                                'announcer result api', 'announcer resource api', 'announcer alert api', 
                                'recovery time out', 'recovery delete time', 'work directory' ]:
                return_message.append("NOK : %s is not config key\n" % _key)
                continue
            if _key in [ 'event flow home', 'console connect address', 'console connect port',
                            'dump dir', 'flask shutdown code' ]:
                return_message.append("NOK : %s is not configurable key\n" % _key)
                continue
            try:
                main_p.config_conn.set(_key, _value)
                return_message.append("OK : [%s] config set to [%s]\n" % (_key, _value))
            except Exception, e:
                return_message.append("NOK : [%s:%s] insert failed in set conf [%s]\n" % ( _key, _value, str(e) ))
                continue
        main_p.config_reload()
        if not web: return MF.make_message(return_message)
        else: return MF.simple_result_json(return_message)
    except Exception, e:
        error_msg = "NOK : Exception occured in set conf [%s]" % str(e) 
        if not web: return MF.make_message(error_msg)
        else: return MF.simple_result_json([error_msg])
