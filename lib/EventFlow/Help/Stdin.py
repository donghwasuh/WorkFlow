shw_hlp_msg = [ \
    "show current stdin status"
    '---',
    '- usage : shw stdin [task name | all]',
    '---',
    '- options',
    '---',
    'no options',
    "---",
    "- example",
    "---",
    ("shw stdin", "show all stdin queue"),
    ("shw stdin ps01", "show ps01's stdin queue")
]

set_hlp_msg = [ \
    'set stdin to dst task',
    '---',
    '- usage : set stdin [task_name]:[send_message], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'set stdin p1:message', "set 'message' to p1's stdin"),
    '---',
    '- description',
    '---',
    '* you can use multiple stdin with "," sep.',
]
    
