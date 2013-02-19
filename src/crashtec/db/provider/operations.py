'''
Created on 02.02.2013

Provides acces to db.    

@author: capone
'''

import psycopg2
from crashtec.config import dbconfig

#TODO: think about error handling for these queries 

class Record (object):
    pass
    
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
    cursor = connection.cursor();
    cursor.execute(sql, params)
    return Cursor(cursor)
    

# param record is instance of class Record
def create_new_record(table, record):
    fields = str()
    placeholders = str()
    arguments = ()
    for property, value in vars(record).iteritems():
        if (fields) :
            fields += ', '
            placeholders += ', '
        fields += property
        placeholders += "%s"
        arguments += (value,)
    sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, fields, placeholders)
    #TODO: log and adapt exception
    exec_sql(sql, arguments)

# execute SELECT sql request and returns Cursor object
def select_from(table_name, field_list = [],  filter = None):
    # TODO: handle field_list
    sql = "select * from %s" % (table_name)
    params = dict()
    if (filter):
        (filter_sql, params) = filter.to_sql()
        sql = "%s where %s" % (sql, filter_sql)
    print sql
    print params
    return exec_sql(sql, params)

