'''
Created on 20.04.2013

@author: capone
'''
import unittest
from mock import MagicMock
import mock

from crashtec.cdbprocessor import resultparsers

class Test01_Parser(unittest.TestCase):
    def test_parse_output(self):
        # Settup mock
        mock_parsers_list = [self.create_parser_mock() for x in range(5)]
        parserObject = resultparsers.Parser(mock_parsers_list)
        # Parse and iterate over results
        results = parserObject.parse_output(None)
        for x in results:
            pass
        # Check 
        for mock_parser in mock_parsers_list:
            mock_parser.parse.assert_called_once_with(None)
    
    def create_parser_mock(self):
        return mock.create_autospec(resultparsers.ModulesSectionParser(),
                             spec_set = True)

# implement it
class Visitor():
    pass

class Test02_Results(unittest.TestCase):
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()