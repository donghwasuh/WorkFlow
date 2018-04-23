import os, sqlite3

import WorkFlow.Common.Conf.Default as DefaultConf
import WorkFlow.Common.Conf.DatabaseHelper as DBHelper

from WorkFlow.Common.Conf.Database import DatabaseBase

class JobDatabase(DatabaseBase):
    def __init__(self):
        DatabaseBase.__init__(self)

    def set(self, job_name, members, schedule):
        query = """
            INSERT INTO JOB_INFO (JOB_NAME, MEMBERS, SCHEDULE) VALUES ('%s', '%s', '%s');
            """ % (job_name, members, schedule)
        self._insert_db( query )

    def get(self, filter_rule):
        return self._select_db(filter_rule)

    def remove(self, job_id):
        self._delete_db( { 'job_id' : job_id } )

    #def rmv_by_task(self, task):
    #    self._delete_db( { 'pname' : task } )

    #def get_by_pname( self, pname ):
    #    return self._select_db( { 'pname' : pname } )

    def list(self):
        return self._select_db({})

if __name__ == '__main__':
    print " - schedule database test code"
    jd = JobDatabase()
    jd.set( 'test_j1', 'f1', '*/1 * * * *' )
    jd.set( 'test_j2', 'f1', '*/1 * * * *' )
    print jd.get( {} )
    jd.remove("1")
    print jd.get( {} )
