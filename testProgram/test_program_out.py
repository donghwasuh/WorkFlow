
import sys
import os
import time
import string
import random

ef_test_program_log = os.environ['EVENTFLOW_HOME'] + "/testProgram/log"
data_set = string.ascii_uppercase + string.digits

try : os.mkdir(ef_test_program_log)
except: pass

process_name = sys.argv[1].strip()

log_fd = open( ef_test_program_log + "/%s.log" % process_name, "a")

log_fd.write(" - process %s started\n" % process_name)

while True:
	out_string = "%s-%s\n" % (process_name, ''.join(random.choice(data_set) for _ in range(5)))
	sys.stdout.write(out_string)
	sys.stdout.flush()
	log_fd.write(" - process %s : stdout : %s\n" % (process_name, out_string))
	time.sleep(1)

