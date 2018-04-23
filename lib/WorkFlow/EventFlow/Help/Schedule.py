shw_hlp_msg = [ \
    "show current schedule setting",
    '---',
    '- usage : shw schedule [options]'
    '---',
    '- options',
    '---',
    ("-t, --task [task name]", "show all schedule which contains task name"),
    ("-f, --time_format [cron time format]", "show all schedule which matched cron time format"),
    "---",
    "- example",
    "---",
    ("shw schedule -t ps01", "show ps01's schedule"),
    ("shw conf -f */1 * * *", "show schedule which has */1 * * * * routine")
]

set_hlp_msg = [ \
    'set new schedule',
    '---',
    '- usage : set schedule [time_format]:[task_name]:[send_message], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'set schedule */1 * * * *:p1:message', ''),
    'set schedule for p1 task, "message" send every 1min',
    '---',
    '- description',
    '---',
    '* you can use multiple flow with "," sep.',
    '* time_format use crontab time format'
]
    
del_hlp_msg = [ \
    'delete schedule info',
    '---',
    '- usage : del schedule [time_format]:[task_name], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'del schedule */1 * * * *:p1', "remove all 1min schedule work with p1"),
    '---',
    '- description',
    '---',
    '* you can use multiple stdin with "," sep.',
    '* time_format use crontab time format'
]
