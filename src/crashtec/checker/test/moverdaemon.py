'''
Created on 13.03.2013

@author: capone
'''

from crashtec.checker import checkerdaemon
import unittest

class TestCheckerImplementation(unittest.TestCase):
    def test_parse_checker_output(self):
        test_data = {'./test_data/x86.txt' : 'win32', './test_data/x64.txt' : 'win64'}
        for file_name, expected in test_data.iteritems():
            impl = checkerdaemon.implementation()
            f = open(file_name, 'rb')
            result = impl.parse_checker_output(f.read())
            self.assertEqual(expected, result['platform'], 'platform value mismatch')
    

if __name__ == '__main__':
    unittest.main()