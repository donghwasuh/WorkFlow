import os


EVENTFLOW_HOME = None

if 'EVENTFLOW_HOME' in os.environ:
    EVENTFLOW_HOME = os.environ['EVENTFLOW_HOME']
    if EVENTFLOW_HOME[-1] == '/': EVENTFLOW_HOME = EVENTFLOW_HOME[:-1]


if __name__ == '__main__':
    print "default test code"
    print EVENTFLOW_HOME
