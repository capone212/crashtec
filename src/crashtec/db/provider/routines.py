'''
Created on 02.02.2013

Provides acces to db.    

@author: capone
'''

import psycopg2
from psycopg2.extras import RealDictCursor
from crashtec.config import dbconfig
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD

#TODO: think about error handling for these queries 

# FIXME: replace simple dict with smart one, 
# which should remember old initial values. 
# Update routine must use this to filter unchanged values, this should 
# reduce amount of data collisions.
Record = dict
    
class Cursor(object):
    def __init__(self, cursor_impl):
        self._cursor_impl = cursor_impl
    
    def fetch_one(self):
        return self._cursor_impl.fetchone()
    
    def fetch_many(self, count):
        return self._cursor_impl.fetchmany(count)
    
    def fetch_all(self):
        return self._cursor_impl.fetchall()

def exec_sql(sql, params):
#    with psycopg2.connect(DSN) as connection:
#        connection.autocommit = True
#        with connection.cursor() as cursor:
#            cursor.execute(sql, params)
    connection = psycopg2.connect(dbconfig.get_connection_url())
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=RealDictCursor);
    cursor.execute(sql, params)
    return Cursor(cursor)
    
# param record is instance of class Record
def create_new_record(table, record):
    fields = str()
    placeholders = str()
    arguments = ()
    for property_id, value in record.iteritems():
        if (fields) :
            fields += ', '
            placeholders += ', '
        fields += property_id
        placeholders += "%s"
        arguments += (value,)
    sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, fields, placeholders)
    #TODO: log and adapt exception
    exec_sql(sql, arguments)

# execute SELECT sql request and returns Cursor object
def select_from(table_name, field_list=[],  db_filter=None, order=None):
    # TODO: handle field_list
    sql = "select * from %s" % (table_name)
    params = dict()
    if (db_filter):
        (filter_sql, params) = db_filter.to_sql()
        sql = "%s where %s" % (sql, filter_sql)
    
    if (order):
        sql = "%s order by %s" % (sql, order.to_sql())
    #print sql , ' | ' , params
    return exec_sql(sql, params)

# TODO: add optional id parameter
def update_record(table, record, key_field = PRIMARY_KEY_FIELD):
    arguments = ()
    fields = str()
    for property_id, value in record.iteritems():
        if property_id == key_field:
            continue
        if (fields) :
            fields += ', '
        fields += '%s=%%s' % property_id
        arguments += (value,)
    sql = 'update %s SET %s WHERE %s = %%s' % (table, fields, key_field)
    arguments += (record[key_field],)
    #print sql, ' | ' , arguments
    return exec_sql(sql, arguments)