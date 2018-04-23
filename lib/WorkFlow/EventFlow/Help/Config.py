shw_hlp_msg = [ \
    "show current configuration status",
    '---',
    '- usage : shw conf [options]',
    '---',
    '- options',
    '---',
    ("-n, --not-changeable", "show not changeable config"),
    ("-c, --changeable", "show changeable config"),
    ("-k, --key [config key]", "show applicable config (support comma sep)"),
    "---",
    "- example",
    "---",
    ("shw conf -n", "show not changeable config"),
    ("shw conf -k flask port", "show 'flask port' config value"),
]

set_hlp_msg = [ \
    'set configuration',
    '---',
    '- usage : set conf [config key]:[config_value], ...',
    '---',
    '- options',
    '---',
    'no options',
    '---',
    '- example',
    '---',
    ( 'set conf flask port:5000', 'set flask port to 5000' ),
    ( 'set conf flask port:5000, ', 'set flask port and run' ),
    ( '         flask run:True', ''),
    '---',
    '- description',
    '---',
    '* you can use multiple config with "," sep.'
]
    
