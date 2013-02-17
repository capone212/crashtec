'''
Created on 02.02.2013

Provides acces to db.    

@author: capone
'''

import psycopg2
from crashtec.config import dbconfig
import psycopg2


class Record (object):
    pass
    
#INSERT INTO films (code, title, did, date_prod, kind)
#    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');

def exec_sql(sql, params):
    # TODO: read params from config file
    DSN = "dbname=crashtec user=postgres password=crashtec"
#    with psycopg2.connect(DSN) as connection:
#        connection.autocommit = True
#        with connection.cursor() as cursor:
#            cursor.execute(sql, params)
    connection = psycopg2.connect(DSN)
    connection.autocommit = True
    cursor = connection.cursor();
    print params
    cursor.execute(sql, params)
    
    
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
    print sql
    #TODO: log and adapt exception
    exec_sql(sql, arguments)
    

