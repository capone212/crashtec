'''
Created on 13.05.2013

@author: capone
'''
import unittest

from mock import MagicMock
from mock import patch
from mock import DEFAULT

from crashtec.db.provider.routines import Record

from crashtec.infrastructure.public import agentutils

CLASS_TYPE = 'class_type'
INSTANCE_NAME = 'instance_name'
GROUP_ID = 'group_id'

@patch.multiple('crashtec.db.provider.routines', 
                exec_sql=DEFAULT, select_from=DEFAULT)
class Test_register_agent(unittest.TestCase):
    def test_register_new_agent_deep_db_check(self, exec_sql, select_from):
        self.build_select_mock(select_from , None)
        agentutils.register_agent(CLASS_TYPE, INSTANCE_NAME, GROUP_ID)
        
        EXPECT_SQL = 'INSERT INTO agents (instance_name, group_id, registered_time, class_type, last_keepalive) VALUES (%s, %s, %s, %s, %s);'       
        (sql, values), keywords = exec_sql.call_args
        self.assertEqual(EXPECT_SQL, sql)
    
    def test_register_update_agent_deep_db_check(self, exec_sql, select_from):
        INITIAL = {'instance_name' : INSTANCE_NAME, 'last_keepalive' : 'keep_alive',
                    'registered_time' : 'time1', 'class_type' : CLASS_TYPE,
                    'id' : 10, 'group_id' : GROUP_ID
                   }
        self.build_select_mock(select_from , Record(INITIAL))
        agentutils.register_agent(CLASS_TYPE, INSTANCE_NAME, GROUP_ID)
        
        EXPECT_SQL = 'update agents SET registered_time=%s, last_keepalive=%s WHERE id = %s'       
        (sql, values), keywords = exec_sql.call_args
        self.assertEqual(EXPECT_SQL, sql)
    
    def build_select_mock(self, select_from, retruns):
        cursor = MagicMock()
        cursor.fetch_one = MagicMock(return_value=retruns)
        select_from.return_value = cursor

@patch('crashtec.db.provider.routines.exec_sql')
class Test_send_keepalive_message(unittest.TestCase):
    def test_send_keepalive_message(self, exec_sql):
        agentutils.send_keepalive_message(INSTANCE_NAME)
        (sql, values), keywords = exec_sql.call_args
        EXPECT_SQL = 'update agents SET last_keepalive=%s WHERE instance_name = %s'
        self.assertEqual(EXPECT_SQL, sql)