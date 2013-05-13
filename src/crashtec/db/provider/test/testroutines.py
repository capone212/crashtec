'''
Created on 12.05.2013

@author: capone
'''
import unittest
from mock import patch
from mock import MagicMock

from crashtec.db.provider.routines import Record
from crashtec.db.provider import routines
from crashtec.utils.exceptions import CtCriticalError

def _get_sample_record():
    return {'key1' : 'value2', 'key2' : 'value2' }

class TestRecord(unittest.TestCase):
    def test01_get_value(self):
        record = Record(_get_sample_record())
        for key, value in _get_sample_record().iteritems():
            self.assertEqual(value, record[key], 'Getter does not work')
    
    def test02_set_values(self):
        record = Record()
        for key, value in _get_sample_record().iteritems():
            record[key] = value
        
        for key, value in _get_sample_record().iteritems():
            self.assertEqual(value, record[key], 'Setter does not work')
    
    def test03_update(self):
        record = Record(_get_sample_record())
        record['mock_key'] = 'mock_value' 
        
        for key, value in _get_sample_record().iteritems():
            self.assertEqual(value, record[key], 'Setter does not work')
        self.assertEqual('mock_value', record['mock_key'],
                          'Setter does not work')
    
    def test04_updated_values(self):
        record = Record(_get_sample_record())
        
        initial = _get_sample_record()
        modifier = {initial.keys()[1] : 'garbage', 'mock_key' : 'mock_value'}
        for key, value in modifier.iteritems():
            record[key] = value
        updated_values = record.updated_values()
        self.assertEqual(updated_values, modifier)
        
        # Modify second time
        modifier2 = {initial.keys()[0] : 'garbage2: reload', 
                     'mock_key2' : 'mock_value2'}
        for key, value in modifier2.iteritems():
            record[key] = value
            
        # Validate
        modifier2.update(modifier)
        updated_values = record.updated_values()
        self.assertEqual(updated_values, modifier2)


class TestCursor(unittest.TestCase):
    def test_fetch_one_returns_record(self):
        # Prepare mock object
        mock_impl = MagicMock(spec_set = ['fetchone'])
        mock_impl.fetchone = MagicMock(return_value = self.get_sample_record())
        # Do test
        cursor = routines.Cursor(mock_impl)
        record = cursor.fetch_one()
        # Validate results
        self.check_equal(record, self.get_sample_record())
    
    def test_fetch_one_returns_none(self):
        # Prepare mock object
        mock_impl = MagicMock(spec_set = ['fetchone'])
        mock_impl.fetchone = MagicMock(return_value = None)
        # Do test
        cursor = routines.Cursor(mock_impl)
        record = cursor.fetch_one()
        # Validate results
        self.assertEqual(record, None)
    
    def test_fetch_many_returns_records(self):
        self.check_fetch_many(5)
    
    def test_fetch_many_returns_empty(self):
        self.check_fetch_many(0)
    
    def test_fetch_all_returns_records(self):
        self.check_fetch_all(5)
    
    def test_fetch_all_returns_empty(self):
        self.check_fetch_all(0)
    
    def check_fetch_many(self, count):
        # Prepare mock object
        mock_impl = MagicMock(spec_set = ['fetchmany'])
        mock_impl.fetchmany = MagicMock(return_value = \
                            (self.get_sample_record() for x in range(count)))
        # Do test
        cursor = routines.Cursor(mock_impl)
        records = cursor.fetch_many(count)
        # Validate results
        mock_impl.fetchmany.assert_called_with(count)
        self.assertEqual(len(records), count)
        for record in records:
            self.check_equal(record, self.get_sample_record())
    
    def check_fetch_all(self, count):
        # Prepare mock object
        mock_impl = MagicMock(spec_set = ['fetchall'])
        mock_impl.fetchall = MagicMock(return_value = \
                            (self.get_sample_record() for x in range(count)))
        # Do test
        cursor = routines.Cursor(mock_impl)
        records = cursor.fetch_all()
        # Validate results
        mock_impl.fetchall.assert_called_with()
        self.assertEqual(len(records), count)
        for record in records:
            self.check_equal(record, self.get_sample_record())
           
    def check_equal(self, record, dict_value):
        self.assertEqual(record.keys(), dict_value.keys(), 
                         'keys are not equal')
        self.assertEqual(record.values(), dict_value.values(), 
                         'values are not equal')
    
    def get_sample_record(self):
        return {'key1':'value1', 'key2':'value2'}
    


@patch('crashtec.db.provider.routines.exec_sql')
class Test_create_new_record(unittest.TestCase):
    def test_with_dictionary(self, pached_exec_sql):
        TABLE_NAME = 'mock_table'
        mock_record = {'field1' : 'value1', 'field2' : 'value2'}
        routines.create_new_record(TABLE_NAME, mock_record)
        EXPECTED_SQL = 'INSERT INTO mock_table (field2, field1) VALUES (%s, %s);'
        
        # Check results
        (sql_string, values), keywords = pached_exec_sql.call_args
        self.assertEqual(EXPECTED_SQL, sql_string,'sql strings does not match')
        self.assertEqual(list(mock_record.values()),
                        list(values))
    def test_with_Record(self, pached_exec_sql):
        TABLE_NAME = 'mock_table'
        mock_record = {'field1' : 'value1', 'field2' : 'value2'}
        routines.create_new_record(TABLE_NAME, Record(mock_record))
        EXPECTED_SQL = 'INSERT INTO mock_table (field2, field1) VALUES (%s, %s);'
        
        # Check results
        (sql_string, values), keywords = pached_exec_sql.call_args
        self.assertEqual(EXPECTED_SQL, sql_string,'sql strings does not match')
        self.assertEqual(list(mock_record.values()),
                        list(values))


@patch('crashtec.db.provider.routines.exec_sql')
class Test_update_record(unittest.TestCase):

    def test_key_field_updated(self, pached_exec_sql):
        record = Record()
        for key, value in self.get_mock_record().iteritems():
            record[key] = value 
        
        (sql_string, values), keywords = self._do_test(record, pached_exec_sql)
        EXPECTED_STRING = 'update mock_table SET field2=%s, field1=%s WHERE id = %s'
        self.assertEqual(EXPECTED_STRING, sql_string)
        self.assertEqual(values, record.values())
        
    
    def test_no_updated_values(self, pached_exec_sql):
        self._do_test(Record(self.get_mock_record()), pached_exec_sql)
        self.assertFalse(pached_exec_sql.called, 'Should not be called')
    
    def test_partial_updated(self, pached_exec_sql):
        record = Record(self.get_mock_record())
        MOCK_VALUE = 'mock_value'
        record['field2'] = MOCK_VALUE
        (sql_string, values), keywords = self._do_test(record, pached_exec_sql)
        # Check results
        EXPECTED_SQL = 'update mock_table SET field2=%s WHERE id = %s'
        self.assertEqual(EXPECTED_SQL, sql_string)
        self.assertEqual([MOCK_VALUE, record['id']], list(values))
    
    def _do_test(self, mock_record, pached_exec_sql):
        MOCK_TABLE_NAME = 'mock_table'
        routines.update_record(MOCK_TABLE_NAME, mock_record)
        return pached_exec_sql.call_args

    def get_mock_record(self):
        return {'id' : 10, 'field1' : 'value1', 'field2' : 'value2'}
    
if __name__ == '__main__':
    unittest.main()