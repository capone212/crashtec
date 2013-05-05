'''
Created on 20.04.2013

@author: capone
'''
import os
import unittest
from mock import MagicMock
import mock

from crashtec.cdbprocessor import resultspublisher
from crashtec.cdbprocessor import resultparsers
 
class Test01_Parser(unittest.TestCase):
    def test01_parse_all_parsers_called(self):
        # Settup mock
        mock_parsers_list = [self._create_parser_mock() for x in range(5)]
        parserObject = resultparsers.Parser(mock_parsers_list)
        # Parse and iterate over results
        results = parserObject.parse_output(None)
        for x in results:
            pass
        # Check 
        for mock_parser in mock_parsers_list:
            mock_parser.parse.assert_called_once_with(None)
    
    def _create_parser_mock(self):
        return mock.create_autospec(resultparsers.ModulesSectionParser(),
                             spec_set = True)

class Test02_CrashSignatureParser(unittest.TestCase):
    def setUp(self):
        self.visitor_called = False
        self.expected_results = None
        
    def test_parse_positive(self):
        PEOCESSED_FILE_NAME = os.path.dirname(__file__) + "/test_data/406/results.txt"
        f = open(PEOCESSED_FILE_NAME, 'r')
        signature_parser = resultparsers.CrashSignatureParser()
        signature = signature_parser.parse(f.read())
        
        self.expected_results = resultparsers.CrashSignature(
                            'NULL_CLASS_PTR_DEREFERENCE', 
                            'ItvSdkUtil.dll', 
                            'itvsdkutil!CCompressedBuffer::CCompressedBuffer+97', 
                            'NULL_CLASS_PTR_DEREFERENCE_c0000005_ItvSdkUtil.dll!CCompressedBuffer::CCompressedBuffer'
                            )
                
        signature.accept(self)
        self.assertTrue(self.visitor_called, "Result object did not call visitor")
    
    def test_parse_negative(self):
        signature_parser = resultparsers.CrashSignatureParser()
        signature = signature_parser.parse('bad input')
        
        self.expected_results = resultparsers.CrashSignature(
                            '', 
                            '', 
                            '', 
                            ''
                            )
                
        signature.accept(self)
        self.assertTrue(self.visitor_called, "Result object did not call visitor")
    
    def visit_CrashSignatureParserResults(self, results):
        self.visitor_called = True
        # A bit dirty, but for unit test it is hopefully OK.
        self.assertEqual(self.expected_results.__dict__, results.__dict__) 
        


class Test02_ResultsVisitor(unittest.TestCase):
    def test_perser_results_support_visitor(self):
        parser = resultparsers.create_parser()
        results = parser.parse_output("doesn't matter what.")
        mock_visitor = mock.create_autospec(resultspublisher.ResultsPublisher(None),
                             spec_set = True)
        for result_item in results:
            result_item.accept(mock_visitor)
        
        self.assertTrue(mock_visitor.visit_ModulesSectionParserResults.called)
        self.assertTrue(mock_visitor.visit_RawOutpuSectionParserResults.called)
        self.assertTrue(mock_visitor.visit_CrashSignatureParserResults.called)
        self.assertTrue(mock_visitor.visit_ProblemStackParserResuls.called) 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()