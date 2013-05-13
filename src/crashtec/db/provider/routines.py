'''
Created on 02.02.2013

Provides acces to db.    

@author: capone
'''

import psycopg2
import itertools
from psycopg2.extras import RealDictCursor
from crashtec.config import dbconfig
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD

from crashtec.utils.exceptions import CtCriticalError

#TODO: think about error handling for these queries 

# FIXME: replace simple dict with smart one, 
# which should remember old initial values. 

class Record(object):
    '''
        Represents database table record (single row)
        
    '''
    
    def __init__(self, value = dict()):
        '''
        Constructor. 
            
        Takes dictionary of initial values, where keys are 
        table field names and mapped values are db field values of current row. 
        '''
        # Holds two copies of initial map, they used to track changed values
        self.initial_values = value.copy()
        self.current_values = value.copy()
    
    def __eq__(self, other):
        return  self.current_values == other.current_values
    
    def __setitem__(self, key, value):
        self.current_values[key] = value
    
    def __getitem__(self, key):
        return self.current_values[key]
    
    def iteritems(self):
        return self.current_values.iteritems()
    
    def keys(self):
        return self.current_values.keys()
    
    def values(self):
        return self.current_values.values()
    
    def updated_values(self):
        ''' 
            Returns a dictionary of updated items.
            
            'Updated items' are items that does not exists or changed 
            in initial map (that was passed in constructor)
        '''
        curents = self.current_values
        olds = self.initial_values
        return {k : v for k, v in curents.iteritems() 
                if (k not in olds) or (v != olds[k])}
        
         
class Cursor(object):
    def __init__(self, cursor_impl):
        self._cursor_impl = cursor_impl
    
    def fetch_one(self):
        fetched = self._cursor_impl.fetchone()
        if not fetched:
            return fetched
        return Record(fetched)
    
    def fetch_many(self, count):
        return [Record(x) for x in self._cursor_impl.fetchmany(count)]
    
    def fetch_all(self):
        return [Record(x) for x in self._cursor_impl.fetchall()]

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
    # TODO: replace tuples with list!
    fields = ', '.join(record.keys())
    placeholders = ', '.join(["%s" for x in range(len(record.keys()))])
    arguments = record.values()
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
    return exec_sql(sql, params)

def update_record(table, record, key_field = PRIMARY_KEY_FIELD):
    updated_values = record.updated_values()
    if not updated_values:
        return
#     if key_field in updated_values.keys():
#         raise CtCriticalError('Key field value is updated.' 
#         'This should be a bug in called module')
    keys = [property_id for property_id in updated_values.keys()
                       if property_id != key_field]
    fields = ', '.join('%s=%%s' %
                       property_id for property_id in keys)
    arguments = [updated_values[key] for key in keys]
    sql = 'update %s SET %s WHERE %s = %%s' % (table, fields, key_field)
    arguments.append(record[key_field])
    return exec_sql(sql, arguments)