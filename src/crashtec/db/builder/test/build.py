import crashtec.db.builder.build as build
import unittest
import crashtec

DB_DESCRIPTION_LIST = [{'task': {'finishTime': 'datetime', 'logFile': 'long_string', 'dumpFileName': 'long_string', 'pubDate': 'datetime', 'resultFile': 'long_string'}}, 
                           {'task': {'finishTime': 'datetime', 'status': 'short_string', 'analyseAgent': 'string', 
                            'pubDate': 'datetime', 'dumpFileName': 'long_string', 'user': 'short_string'}}]
        

class TestSequenceFunctions(unittest.TestCase):
    
    def test_collect_model_descriptions(self):
        components_list = ["testData.comp1", "testData.comp2"]        
        model_descriptions = build.collect_model_descriptions(components_list)
        exceptionList = DB_DESCRIPTION_LIST
        self.assertEqual(model_descriptions, exceptionList)

    def test_agregate_descriptions(self):
        aggregated_result = build.agregate_descriptions(DB_DESCRIPTION_LIST)
        EXPECTED_RESULT = {'task': {'finishTime': 'datetime', 'status': 'short_string', 'analyseAgent': 'string', 
                                    'pubDate': 'datetime', 'dumpFileName': 'long_string', 'user': 'short_string', 
                                    'logFile': 'long_string', 'resultFile': 'long_string'}}
        self.assertEqual(aggregated_result, EXPECTED_RESULT)
        

if __name__ == '__main__':
    unittest.main()
