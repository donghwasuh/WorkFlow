import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class ArrowDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, arrow_name, flow_id, arrow):
        query = """
            INSERT INTO ARROW_INFO (ARROW_NAME, FLOW_ID, ARROW) \
            VALUES ( '%s',' %s', '%s' );
            """  % (arrow_name, flow_id, arrow)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self,arrow_id):
        self._delete_db( { 'arrow_id' : arrow_id } )

    #def get_by_name(self, name):
    #    return self._select_db( { 'QUERY' : "( flow_from = '%s' or flow_to = '%s' )" % ( name, name ) } )

    #def get_by_type(self, flow_type):
    #    return self._select_db( { 'flow_type' : type_name } )

    def list(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - arrow database test code"
    ad = ArrowDatabase()
    ad.set('testa1', 'f1', 'a->b')
    ad.set('testa2', 'f1', 'a->b->c')
    ad.set('testa3', 'f1', 'a->b->c')

    print ad.get('')
    print ad.list()
    print 

    ad.remove('1')
    ad.remove('2')
    ad.remove('3')
    
    print ad.get('')
    print ad.list()
    print 
    
