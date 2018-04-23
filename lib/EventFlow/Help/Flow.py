shw_hlp_msg = [ \
    "show current flow setting",
    '---',
    '- usage : shw flow [options]',
    '---',
    '- options',
    '---',
    ("-t, --task [task name]", "show all flow info which contains task name"),
    ("-f, --flow_type [share|broad]", "show all flow with flow type"),
    "---",
    "- example",
    "---",
    ("shw conf -t ps01", "show flow applicable ps01 task"),
    ("shw conf -f broad", "show broad flow")
]

set_hlp_msg = [ \
    'set new flow',
    '---',
    '- usage : set flow [flow_type]:[flow_from]:[flow_to], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'set flow share:ps01:ps02', 'set share flow ps01 to ps02'),
    ( 'set flow broad:ps01:ps02|ps03', 'set broad flow ps01 to ps02 and ps03'),
    '---',
    '- description',
    '---',
    '* you can use multiple [flow_from] and [flow_to] with "|" sep.',
    '* you can use multiple flow with "," sep.'
]
    
del_hlp_msg = [ \
    'del existing flow',
    '---',
    '- usage : set flow [flow_type]:[flow_from]:[flow_to], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'del flow broad:p1:p2', "delete broad flow that p1 to p2"),
    '---',
    '- description',
    '---',
    '* you can use multiple [flow_from] and [flow_to] with "|" sep.',
    '* you can use multiple stdin with "," sep.',
]
