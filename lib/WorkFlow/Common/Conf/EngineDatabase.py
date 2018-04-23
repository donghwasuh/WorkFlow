import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class EngineDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, engine_name, ip, port):
        query = """
            INSERT INTO ENGINE_INFO (ENGINE_NAME, IP, PORT) VALUES ( '%s',' %s', '%s' );
            """  % (engine_name, ip, port)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self, engine_id):
        self._delete_db( { 'engine_id' : engine_id } )

    def get_by_name(self, process_name):
        return self.get( { 'pname' : process_name } )

    def get_by_type(self, process_type):
        return self.get( { 'ptype' : process_type } )

    def list(self):
        return self.get({})


if __name__ == '__main__':
    print " - engine database test code"
    ed = EngineDatabase()
    ed.set("test_e", "192.168.100.180", "9292")
    print ed.get("")
    ed.remove("1")
    print ed.get("")
    

