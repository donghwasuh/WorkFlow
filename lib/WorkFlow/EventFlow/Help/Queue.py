shw_hlp_msg = [ \
    "show current global queue"
    '---',
    '- usage : shw global_queue',
    '---',
    '- options',
    '---',
    'no option',
    "---",
    "- example",
    "---",
    ("shw global_queue", "show global queue")
]

del_task_queue_hlp_msg = [ \
    "delete task's queue info",
    '---',
    '- usage : del task_queue [task_name], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'del task_queue p1', "remove all queue which located p1 task"),
    '---',
    '- description',
    '---',
    '* you can use multiple task name with "," sep.',
    '* time_format use crontab time format'
]
lad_queue_hlp_msg = [ \
    "load task's queue from dump file",
    '---',
    '- usage : lad [task_name], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'lad p1', "load 'p1' task's queue from 'p1' dump file"),
    '---',
    '- description',
    '---',
    '* you can use multiple task name with "," sep.',
]
sav_queue_hlp_msg = [ \
    "save task's queue to dump file",
    '---',
    '- usage : sav [task_name], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'sav p1', "save 'p1' task's queue to 'p1' dump file"),
    '---',
    '- description',
    '---',
    '* you can use multiple task name with "," sep.',
]
