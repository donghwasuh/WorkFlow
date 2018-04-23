import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class TaskDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, task_name, command, engine_id, output_type='broad', is_daemon='False', description='None'):
        query = """
            INSERT INTO TASK_INFO (TASK_NAME, COMMAND, ENGINE_ID, IS_DAEMON, OUTPUT_TYPE, \
            DESCRIPTION) VALUES ( '%s',' %s', '%s', '%s', '%s', '%s' );
            """  % (task_name, command, engine_id, output_type, is_daemon, description)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self, task_id):
        self._delete_db( { 'task_id' : task_id } )

    #def get_by_name(self, name):
    #    return self._select_db( { 'QUERY' : "( flow_from = '%s' or flow_to = '%s' )" % ( name, name ) } )

    #def get_by_type(self, flow_type):
    #    return self._select_db( { 'flow_type' : type_name } )

    def list(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - flow database test code"
    td = TaskDatabase()
    td.set('task1', 'python..', 'e1')
    td.set('task2', 'python..', 'e2', 'shared')
    td.set('task3', 'python..', 'e2', 'shared', 'True')
    td.set('task4', 'python..', 'e2', 'shared', 'True', 'test description')
    print
    print td.list()
    print td.get("")
    print
    td.remove('1')
    td.remove('2')
    td.remove('3')
    print
    print td.list()
    print td.get("")
    
