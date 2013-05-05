'''
Created on 13.03.2013

@author: capone
'''
import unittest
import os

from crashtec.checker import checker

def _get_full_path(relative_path):
    return os.path.join(os.path.dirname(__file__), 
                 relative_path)
    
class TestCheckerImplementation(unittest.TestCase):
    def test_01_parse_checker_output(self):
        test_data = {'test_data/x86.txt' : 'win32', 
                     'test_data/x64.txt' : 'win64'}
        for file_name, expected in test_data.iteritems():
            impl = checker.Implementation()
            f = open(_get_full_path(file_name), 'rb')
            result = impl.parse_checker_output(f.read())
            self.assertEqual(expected, result['platform'], 
                             'platform value mismatch')
    
    def test_02_execute_dump_checker(self):
        dump_file_name = _get_full_path('test_data\\dump.dmp')
        impl = checker.Implementation()
        checker_out = impl.execute_dump_checker(dump_file_name)
        result = impl.parse_checker_output(checker_out)
        self.assertTrue(result, 'Result should not be empty')

if __name__ == '__main__':
    unittest.main()