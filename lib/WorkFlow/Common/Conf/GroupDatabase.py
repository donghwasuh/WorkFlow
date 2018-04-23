import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class GroupDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, group_name, members):
        query = """
            INSERT INTO GROUP_INFO (GROUP_NAME, MEMBERS) VALUES ( '%s',' %s' );
            """  % (group_name, members)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self, group_id):
        self._delete_db( { 'group_id' : group_id } )

    def list(self):
        return self._select_db({})
        
if __name__ == '__main__':
    print " - group database test code"
    gd = GroupDatabase()
    gd.set("test_g1", "t1, t2",)
    gd.set("test_g2", "t1, t2",)
    print gd.get("")
    gd.remove("1")
    print gd.get("")
    print gd.list()
