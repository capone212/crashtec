'''
Created on 02.02.2013

@author: capone

Contains db connection information 
'''

# TODO: rewrite using this
"""
Here's yet another way:

def enum(**enums):
    return type('Enum', (), enums)

Used like so:

>>> Numbers = enum(ONE=1, TWO=2, THREE='three')
>>> Numbers.ONE
1
>>> Numbers.TWO
2
>>> Numbers.THREE
'three'
"""

DB_NAME_PARAM = 'dbname'
USER_NAME_PARAM = 'user_name'
PASSWORD_PARAM = "password"
SERVER_NAME_PARAM = 'server'
PORT_PARAM = 'port'

db_connection_info = {   
    SERVER_NAME_PARAM : 'localhost',
    PORT_PARAM : '5432',
    #PORT_PARAM : '49998',
    DB_NAME_PARAM : 'crashtec',
    USER_NAME_PARAM : "postgres",
    PASSWORD_PARAM : 'crashtec'
    #PASSWORD_PARAM: ''
}

def get_connection_url():
    return "host=%s port=%s dbname=%s user='%s' password='%s'" % (
                db_connection_info[SERVER_NAME_PARAM],
                db_connection_info[PORT_PARAM],
                db_connection_info[DB_NAME_PARAM],
                db_connection_info[USER_NAME_PARAM],
                db_connection_info[PASSWORD_PARAM]
                )