import os, sqlite3

import EventFlow.Conf.Default as DefaultConf
import EventFlow.Conf.DatabaseHelper as DBHelper

from EventFlow.Conf.Database import DatabaseBase

class ScheduleDatabase(DatabaseBase):
    def __init__(self, node_name):
        DatabaseBase.__init__(self, node_name)

    def set(self, scheduled_time, pname, message):
        self._insert_db( ( scheduled_time, pname, message ) )

    def rmv(self, scheduled_time, task):
        self._delete_db( { 'scheduled_time' : scheduled_time, 'pname' : task } )

    def rmv_by_task(self, task):
        self._delete_db( { 'pname' : task } )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def get_by_pname( self, pname ):
        return self._select_db( { 'pname' : pname } )

    def lst(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - schedule database test code"
    sd = ScheduleDatabase("test")
    sd.set( '*/1 * * * *', 'test_p', 'test process message' )
    sd.set( '*/2 * * * *', 'test_p', 'test process message' )
    print sd.get( {} )
    print sd.get( { 'scheduled_time' : '*/1 * * * *' } )
    print sd.lst()
