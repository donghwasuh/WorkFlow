import EventFlow.Help.Config as config_help
import EventFlow.Help.Task as task_help
import EventFlow.Help.Flow as flow_help
import EventFlow.Help.Group as group_help
import EventFlow.Help.Stdin as stdin_help
import EventFlow.Help.Schedule as schedule_help
import EventFlow.Help.Queue as queue_help


h_message_set = {}
h_message_set['hlp'] = {}
h_message_set['hlp'][None] = [ \
( 'shw', 
'''show data command
---sub command list
conf, task, flow, group, stdin, schedule, global_queue, status, recovery, ready''', 
'shw [sub command] [args]', 
'multi-line' ),
( 'set',
'''set data command
---sub command list
conf, task, flow, group, stdin, schedule, recovery''',
'set [sub command] [args]',
'multi-line' ),
( 'del',
'''del data command
---sub command list
task, flow, group, stdin, schedule, task_queue''',
'del [sub command] [args]',
'multi-line' ),
('lad',     'load queue from file',     'lad [args]',   'multi-line' ),
('sav',     'save queue to file',       'sav [args]',   'multi-line' ),
('act',     'act task',                 'act [args]',   'multi-line' ),
('trm',     'trm task',                 'trm [args]',   'multi-line' ),
('q, quit', 'quit this session',        'quit',         '"BYE"' ),
('k, kil',  'kill event flow process',  'kil',          '"BYE"')
]
h_message_set['shw'] = {}
h_message_set['shw'][None] = [ \
( 'conf',           'show configuration info',  'shw conf [args]',          'multi-line' ),
( 'task',           'show task info',           'shw task [args]',          'multi-line' ),
( 'flow',           'show flow info',           'shw flow [args]',          'multi-line' ),
( 'group',          'show group info',          'shw group [args]',         'multi-line' ),
( 'stdin',          'show stdin info',          'shw stdin [args]',         'multi-line' ),
( 'schedule',       'show schedule info',       'shw schedule [args]',      'multi-line' ),
( 'global_queue',   'show global_queue info',   'shw global_queue [args]',  'multi-line' ),
( 'status',         'show status info',         'shw status [args]',        'multi-line' ),
( 'recovery',       'show recovery info',       'shw recovery [args]',      'multi-line' ),
( 'ready',          'show ready info',          'shw ready [args]',         'multi-line' )
]
h_message_set['shw']['conf']            = config_help.shw_hlp_msg
h_message_set['shw']['task']            = task_help.shw_hlp_msg
h_message_set['shw']['flow']            = flow_help.shw_hlp_msg
h_message_set['shw']['group']           = group_help.shw_hlp_msg
h_message_set['shw']['stdin']           = stdin_help.shw_hlp_msg
h_message_set['shw']['schedule']        = schedule_help.shw_hlp_msg
h_message_set['shw']['global_queue']    = queue_help.shw_hlp_msg
h_message_set['shw']['status']          = task_help.shw_status_hlp_msg
h_message_set['shw']['recovery']        = task_help.shw_recovery_hlp_msg
h_message_set['shw']['ready']           = task_help.shw_ready_hlp_msg

h_message_set['set'] = {}
h_message_set['set'][None] = [ \
( 'conf',       'set configuration',            'set conf [args]',      'multi-line' ),
( 'task',       'set new task',                 'set task [args]',      'multi-line' ),
( 'flow',       'set new flow',                 'set flow [args]',      'multi-line' ),
( 'group',      'set group',                    'set group [args]',     'multi-line' ),
( 'stdin',      'put stdin message to task',    'set stdin [args]',     'multi-line' ),
( 'schedule',   'set new schedule',             'set schedule [args]',  'multi-line' ),
( 'recovery',   'run recovery',                 'set recovery [args]',  'multi-line' ),
]
h_message_set['set']['conf']        = config_help.set_hlp_msg
h_message_set['set']['task']        = task_help.set_hlp_msg
h_message_set['set']['flow']        = flow_help.set_hlp_msg
h_message_set['set']['group']       = group_help.set_hlp_msg
h_message_set['set']['stdin']       = stdin_help.set_hlp_msg
h_message_set['set']['schedule']    = schedule_help.set_hlp_msg
h_message_set['set']['recovery']    = task_help.set_recovery_hlp_msg

h_message_set['del'] = {}
h_message_set['del'][None] = [ \
( 'task',       'del task',                     'del task [args]',          'multi-line' ),
( 'flow',       'del flow',                     'del flow [args]',          'multi-line' ),
( 'group',      'del group',                    'del group [args]',         'multi-line' ),
( 'schedule',   'del schedule',                 'del schedule [args]',      'multi-line' ),
( 'task_queue', 'del task_queue',               'del task_queue [args]',    'multi-line' ),
]
h_message_set['del']['task']        = task_help.del_hlp_msg
h_message_set['del']['flow']        = flow_help.del_hlp_msg
h_message_set['del']['group']       = group_help.del_hlp_msg
h_message_set['del']['schedule']    = schedule_help.del_hlp_msg
h_message_set['del']['task_queue']  = queue_help.del_task_queue_hlp_msg

h_message_set['lad'] = {}
h_message_set['lad'][None] = queue_help.lad_queue_hlp_msg
h_message_set['sav'] = {}
h_message_set['sav'][None] = queue_help.sav_queue_hlp_msg
h_message_set['act'] = {}
h_message_set['act'][None] = task_help.act_hlp_msg
h_message_set['trm'] = {}
h_message_set['trm'][None] = task_help.trm_hlp_msg



def help_msg(main, sub):
    message_list = []
    message_list.append('=' * 100)
    if not sub and main not in [ 'act', 'trm', 'lad', 'sav' ]:
        message_list.append( "%s help" % main)
        message_list.append('=' * 100)
        default_prefix_header = '%15s | %30s | %30s | %15s'
        default_prefix = '%-15s | %-30s | %30s | %15s'
        message_list.append(default_prefix_header % ('cmd', 'description', 'command format', 'answer format'))
        for item in h_message_set[main][sub]:
            message_list.append('-' * 100)
            command, description_item, cformat, aformat = item
            first_line_flag = True
            for description in description_item.split('\n'):
                if description.startswith('---'): 
                    message_list.append( default_prefix % ('', '-' * 30, '', '') )
                    description = description.replace('---', '')
                while True:
                    temp_description = description[:30]
                    description = description[30:]
                    if first_line_flag:
                        message_list.append( default_prefix % (command, temp_description, cformat, aformat) )
                        first_line_flag = False
                    else:
                        message_list.append( default_prefix % ('', temp_description, '', '') )
                    if len(description) == 0: break
    else:
        message_list.append( "%s %s help" % (main, sub))
        message_list.append('=' * 100)
        for item in h_message_set[main][sub]:
            if type(item) == type(''):
                if item == '---':
                    message_list.append("-" * 100)
                else:
                    message_list.append(item)
            else:
                prefix = "%-30s : %66s"
                message_list.append(prefix % item)
    message_list.append('=' * 100)
    return '\n'.join(message_list)




if __name__ == '__main__':
    import sys
    main = sys.argv[1]
    try: sub = sys.argv[2]
    except: sub = None

    print help_msg(main, sub)
