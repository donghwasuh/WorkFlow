import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class ConfigDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, config_key, config_value):
        self._insert_replace_db( ( config_key, config_value ) )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def get_by_key(self, key):
        return self._select_db( { 'config_key' : key } )[0]

    def lst(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - config database test code"
    cd = ConfigDatabase()
    cd.set( 'test', 'test' )
    print cd.get({})
    cd.set( 'test', 'test1' )
    print cd.get({})
    cd.set( 'test1', 'test1' )
    print cd.get_by_key('test')
