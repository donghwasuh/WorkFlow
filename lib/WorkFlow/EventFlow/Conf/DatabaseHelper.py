queryDict = {}

queryDict['DEFAULT'] = {}
queryDict['DEFAULT']['CREATE'] = 'CREATE TABLE %s ( %s );'
queryDict['DEFAULT']['CREATE_INDEX'] = 'CREATE INDEX %s_%s_INDEX ON %s ( %s );'
queryDict['DEFAULT']['INSERT'] = 'INSERT INTO  %s ( %s ) values ( %s );'
queryDict['DEFAULT']['INSERT_REPLACE'] = 'INSERT OR REPLACE INTO %s ( %s ) values ( %s );'
queryDict['DEFAULT']['DELETE'] = 'DELETE FROM %s WHERE %s;'
queryDict['DEFAULT']['SELECT'] = 'SELECT * FROM %s WHERE %s;'

queryDict['node'] = {}
queryDict['node']['column']         = [ 'ptype', 'pname', 'pcommand' ]
queryDict['node']['column_type']    = [ 'text', 'text', 'text' ]
queryDict['node']['index']          = [ 'ptype' ]

queryDict['config'] = {}
queryDict['config']['column']         = [ 'config_key', 'config_value' ]
queryDict['config']['column_type']    = [ 'text primary key', 'text' ]
queryDict['config']['index']          = [ 'config_key' ]

queryDict['flow'] = {}
queryDict['flow']['column']         = [ 'flow_type', 'flow_from', 'flow_to' ]
queryDict['flow']['column_type']    = [ 'text', 'text', 'text' ]

queryDict['schedule'] = {}
queryDict['schedule']['column']         = [ 'scheduled_time', 'pname', 'message' ]
queryDict['schedule']['column_type']    = [ 'text', 'text', 'text' ]

queryDict['group'] = {}
queryDict['group']['column']         = [ 'group_name', 'task_name' ]
queryDict['group']['column_type']    = [ 'text', 'text' ]
