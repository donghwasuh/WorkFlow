import os, sqlite3

import EventFlow.Conf.Default as DefaultConf
import EventFlow.Conf.DatabaseHelper as DBHelper


class DatabaseBase:
    def __init__(self, node_name):
        self.path = DefaultConf.EVENTFLOW_HOME + '/data/' + node_name
        self.db_path = self.path + "/%s.db" % self._get_key()
        self.table_name = self._get_key() + '_info'
        self._make_db_directory()
        self._create_db()

    def _make_db_directory(self):
        try: os.makedirs(self.path)
        except: pass

    def _get_key(self):
        return self.__class__.__name__.replace("Database", "").lower()

    def _run_query(self, query, commit=True):
        data = None
        try:
            connect = sqlite3.connect(self.db_path)
            cursor = connect.cursor()
            cursor.execute(query)
            if commit: 
                connect.commit()
                data = True
            else: data = cursor.fetchall()
            connect.close()
        except Exception, e:
            try: connect.close()
            except: pass
            if commit: data = False
            else: data = None
        return data

    def _value_string_maker(self, data):
        value_string = ''
        for i in range(len(data)):
            if len(value_string) != 0: value_string = value_string + ', '
            if DBHelper.queryDict[self._get_key()]['column_type'][i].strip().split()[0] == 'text':
                value_string = value_string + "'" + data[i] + "'"
            else:
                value_string = value_string + data[i]
        return value_string
            
    def _create_db(self):
        if not os.path.exists(self.db_path):
            query_param = ''
            for i in range(len(DBHelper.queryDict[self._get_key()]['column'])):
                if i != 0 and \
                    i != len(DBHelper.queryDict[self._get_key()]['column']) :
                    query_param = query_param + ', '
                query_param = query_param + \
                    DBHelper.queryDict[self._get_key()]['column'][i] + ' ' + \
                    DBHelper.queryDict[self._get_key()]['column_type'][i]
            query = DBHelper.queryDict['DEFAULT']['CREATE'] % ( self.table_name, query_param )
            if not self._run_query(query): raise Exception, "create %s_info table failed." % self._get_key()
            if 'index' in DBHelper.queryDict[self._get_key()]:
                for index_column in DBHelper.queryDict[self._get_key()]['index']:
                    query = DBHelper.queryDict['DEFAULT']['CREATE_INDEX'] % ( self.table_name, index_column, self.table_name, index_column )
                    if not self._run_query(query): raise Exception, "create %s_info index failed." % self._get_key()

    def _insert_db(self, data):
        if len(data) != len(DBHelper.queryDict[self._get_key()]['column']): raise Exception, 'insert failed. data length does not matched.'
        query = DBHelper.queryDict['DEFAULT']['INSERT'] % ( self.table_name, \
                                                            ",".join(DBHelper.queryDict[self._get_key()]['column']), \
                                                            self._value_string_maker(data) )
        if not self._run_query(query): raise Exception, "insert into %s_info failed. [ data : %s ]" % str(data)

    def _insert_replace_db(self, data):
        if len(data) != len(DBHelper.queryDict[self._get_key()]['column']): raise Exception, 'insert / update failed. data lenght does not matched.'
        query = DBHelper.queryDict['DEFAULT']['INSERT_REPLACE'] % ( self.table_name, \
                                                            ",".join(DBHelper.queryDict[self._get_key()]['column']), \
                                                            self._value_string_maker(data) )
        if not self._run_query(query): raise Exception, "insert into %s_info failed. [ data : %s ]" % str(data)

    def _delete_db(self, data):
        if len(data) == 0: raise Exception, 'all delete does not support. target data is not setted'
        query_param = ''
        for item in data:
            if len(query_param) != 0: query_param = query_param + ' AND '
            query_param = query_param + item + " = '%s'" % data[item]
        query = DBHelper.queryDict['DEFAULT']['DELETE'] % ( self.table_name, query_param )
        print query
        if not self._run_query(query): raise Exception, "delete from %s_info failed. [ data : %s ]" % str(data)

    def _select_db(self, data):
        query_param = ''
        for item in data:
            if len(query_param) != 0: query_param = query_param + ' AND '
            if item.upper() == 'QUERY':
                query_param = query_param + data[item]
            else:
                query_param = query_param + item + " = '%s'" % data[item]
        if len(query_param) == 0: query_param = "1 = 1"
        query = DBHelper.queryDict['DEFAULT']['SELECT'] % ( self.table_name, query_param )
        return_data = self._run_query(query, commit=False)
        if return_data == None: raise Exception, "select from %s_info failed. [ data : %s ]" % str(data)
        return return_data

if __name__ == '__main__':
    print " - database test code"
    #nd = NodeDatabase("test")
    #nd.set( 'test', 'test', 'test' )
    #nd.set( 'test1', 'test2', 'test3' )
    #nd.rmv( 'test2' )
    #print nd.get({})
    #print nd.get_by_name('test2')
    cd = ConfigDatabase("test")
    cd.set( 'test', 'test' )
    print cd.get({})
    cd.set( 'test', 'test1' )
    print cd.get({})
    cd.set( 'test1', 'test1' )
    print cd.get_by_key('test')
