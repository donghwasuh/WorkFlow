import os, sqlite3

import EventFlow.Conf.Default as DefaultConf
import EventFlow.Conf.DatabaseHelper as DBHelper

from EventFlow.Conf.Database import DatabaseBase

class FlowDatabase(DatabaseBase):
    def __init__(self, node_name):
        DatabaseBase.__init__(self, node_name)

    def set(self, flow_type, flow_from, flow_to):
        self._insert_db( ( flow_type, flow_from, flow_to ) )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def rmv(self, flow_type, flow_from, flow_to):
        self._delete_db( { 'flow_type' : flow_type, 'flow_from' : flow_from, 'flow_to' : flow_to } )

    def get_by_name(self, name):
        return self._select_db( { 'QUERY' : "( flow_from = '%s' or flow_to = '%s' )" % ( name, name ) } )

    def get_by_type(self, type_name):
        return self._select_db( { 'flow_type' : type_name } )

    def lst(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - flow database test code"
    fd = FlowDatabase("test")
    fd.set( 'BROAD', 'a', 'b' )
    print fd.get_by_name('a')
    fd.set( 'SHARE', 'b', 'a' )
    print fd.get_by_name('a')
    fd.set( 'SHARE', 'b', 'c' )
    print fd.get_by_name('c')
    print fd.get_by_type('BROAD')
    print fd.lst()
