import threading, time, collections, subprocess, sys, os, psutil, zipfile


import EventFlow.Task as Task

from EventFlow.Task.DefaultTask import DefaultTask as DefaultTask
from EventFlow.Task.DefaultTask import DefaultTaskHelper as DefaultTaskHelper
from EventFlow.Task.DefaultTask import DefaultTaskDelHelper as DefaultTaskDelHelper
from EventFlow.Task.ProcessTask import ProcessTask as ProcessTask


name = 'ProcessTask'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

def exceptionLog(msg):
    __LOG__.Trace("E : %s : %s" % (name, msg))
    __LOG__.Exception()

class TalendTaskDelHelper(DefaultTaskDelHelper):
    def __init__(self, main_p, name):
        DefaultTaskDelHelper.__init__(self, main_p, name)

class TalendTaskHelper(DefaultTaskHelper):
    def __init__(self, main_process, name, command, file_name, enc_data):
        DefaultTaskHelper.__init__(self, main_process, name, command, file_name, enc_data)

    def _get_default_path(self):
        return self.main_p.home_path + '/data/' + self.main_p.name + '/bin/talend'

    def _do_specific(self):
        zip_ref = zipfile.ZipFile(self.save_path, 'r')
        zip_ref.extractall(self.default_path)
        zip_ref.close()

    def _replace_command(self):
        temp_file_name = self.file_name.strip().split('.', 1)[0].strip().rsplit('_', 1)[0]
        return 'sh ' + self.default_path + '/%s/%s_run.sh --context_param job_home=%s' % ( temp_file_name, temp_file_name, self.main_p.work_directory + '/%s' % self.name )

class TalendTask(ProcessTask):
    def __init__(self, pname, command, main_process, debugMode=False, recoveryMode=False):
        ProcessTask.__init__(self, pname, command, main_process, debugMode=debugMode, recoveryMode=recoveryMode)

