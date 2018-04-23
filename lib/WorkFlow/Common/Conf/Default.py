import os

WORKFLOW_HOME = None

if 'WORKFLOW_HOME' in os.environ:
    WORKFLOW_HOME = os.environ['WORKFLOW_HOME']
    if WORKFLOW_HOME[-1] == '/': WORKFLOW_HOME = WORKFLOW_HOME[:-1]


if __name__ == '__main__':
    print "default test code"
    print WORKFLOW_HOME
