import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class FlowDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, flow_name, members):
        query = """
            INSERT INTO FLOW_INFO (FLOW_NAME, MEMBERS) VALUES ( '%s',' %s' );
            """  % (flow_name, members)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self, flow_id):
        self._delete_db( { 'flow_id' : flow_id } )

    #def get_by_name(self, name):
    #    return self._select_db( { 'QUERY' : "( flow_from = '%s' or flow_to = '%s' )" % ( name, name ) } )

    #def get_by_type(self, flow_type):
    #    return self._select_db( { 'flow_type' : type_name } )

    def list(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - flow database test code"
    fd = FlowDatabase()
    fd.set("test_f", "t1, t2",)
    print fd.get("")
    fd.remove("1")
    print fd.get("")
    
