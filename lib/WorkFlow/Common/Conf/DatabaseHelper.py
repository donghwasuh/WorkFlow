queryDict = {}

queryDict['DEFAULT'] = {}
queryDict['DEFAULT']['CREATE'] = 'CREATE TABLE %s ( %s );'
queryDict['DEFAULT']['CREATE_INDEX'] = 'CREATE INDEX %s_%s_INDEX ON %s ( %s );'
queryDict['DEFAULT']['INSERT'] = 'INSERT INTO  %s ( %s ) values ( %s );'
queryDict['DEFAULT']['INSERT_REPLACE'] = 'INSERT OR REPLACE INTO %s ( %s ) values ( %s );'
queryDict['DEFAULT']['DELETE'] = 'DELETE FROM %s WHERE %s;'
queryDict['DEFAULT']['SELECT'] = 'SELECT * FROM %s WHERE %s;'

queryDict['engine'] = {}
queryDict['engine']['column']         = [ 'engine_id', 'engine_name', 'ip', 'port' ]
queryDict['engine']['column_type']    = [ 'integer primary key autoincrement', 'text', 'text', 'text', 'text']
queryDict['engine']['index']          = [ 'engine_id' ]

queryDict['job'] = {}
queryDict['job']['column']         = [ 'job_id', 'job_name', 'members', 'control', 'schedule', 'activity', 'create_time', 'update_time' ]
queryDict['job']['column_type']    = [ 'integer primary key autoincrement', 'text', 'text', 'text', 'text', 'text', 'text', 'text']
queryDict['job']['index']          = [ 'job_id' ]

queryDict['group'] = {}
queryDict['group']['column']         = [ 'group_id', 'group_name', 'members', 'job_id', 'create_time', 'update_time' ]
queryDict['group']['column_type']    = [ 'integer primary key autoincrement', 'text', 'text', 'text', 'text', 'text']
queryDict['group']['index']          = [ 'group_id' ]

queryDict['flow'] = {}
queryDict['flow']['column']         = [ 'flow_id', 'flow_name', 'members', 'job_id', 'group_id', 'create_time', 'update_time' ]
queryDict['flow']['column_type']    = [  'integer primary key autoincrement' , 'text', 'text', 'text', 'text', 'text', 'text']
queryDict['flow']['index']          = [ 'flow_id' ]

queryDict['task'] = {}
queryDict['task']['column']         = [ 'task_id', 'task_name', 'command', 'engine_id', 'is_daemon', 'output_type', 'description' ]
queryDict['task']['column_type']    = [ 'integer primary key autoincrement', 'text', 'text', 'text', 'text', 'text', 'text']
queryDict['task']['index']          = [ 'task_id' ]

queryDict['arrow'] = {}
queryDict['arrow']['column']         = [ 'arrow_id', 'arrow_name', 'arrow_type', 'arrow', 'flow_id', 'create_time', 'update_time' ]
queryDict['arrow']['column_type']    = [ 'integer primary key autoincrement' ,'text', 'text', 'text', 'text', 'text', 'text']
queryDict['arrow']['index']          = [ 'arrow_id' ]

queryDict['config'] = {}
queryDict['config']['column']         = [ 'config_key', 'config_value' ]
queryDict['config']['column_type']    = [ 'text primary key', 'text' ]
queryDict['config']['index']          = [ 'config_key' ]
