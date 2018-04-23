import os, sqlite3

import EventFlow.Conf.Default as DefaultConf
import EventFlow.Conf.DatabaseHelper as DBHelper

from EventFlow.Conf.Database import DatabaseBase

class GroupDatabase(DatabaseBase):
    def __init__(self, node_name):
        DatabaseBase.__init__(self, node_name)

    def set(self, group_name, task_name):
        self._insert_db( ( group_name, task_name ) )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def rmv(self, group_name, task_name):
        self._delete_db( { 'group_name' : group_name, 'task_name' : task_name } )

    def lst(self):
        return self._select_db({})
