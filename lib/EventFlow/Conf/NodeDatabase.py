import os, sqlite3

import EventFlow.Conf.Default as DefaultConf
import EventFlow.Conf.DatabaseHelper as DBHelper

from EventFlow.Conf.Database import DatabaseBase

class NodeDatabase(DatabaseBase):
    def __init__(self, node_name):
        DatabaseBase.__init__(self, node_name)

    def set(self, ptype, pname, pcommand):
        self._insert_db( (ptype, pname, pcommand) )

    def rmv(self, pname):
        self._delete_db( { 'pname' : pname } )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def get_by_name(self, process_name):
        return self.get( { 'pname' : process_name } )

    def get_by_type(self, process_type):
        return self.get( { 'ptype' : process_type } )

    def lst(self):
        return self.get({})





if __name__ == '__main__':
    print " - node database test code"
    nd = NodeDatabase("test")
    nd.set( 'test', 'test', 'test' )
    nd.set( 'test1', 'test2', 'test3' )
    nd.rmv( 'test2' )
    print nd.get({})
    print nd.get_by_name('test2')
