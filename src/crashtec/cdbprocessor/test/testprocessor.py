'''
Created on 15.04.2013

@author: capone
'''
import unittest
import os

from mock import MagicMock
from mock import patch
import mock
from crashtec.utils.exceptions import  CtGeneralError

from crashtec.utils.exceptions import CtBaseException
from crashtec.db.provider.routines import Record
from crashtec.infrastructure.public import definitions as infradefs
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD

from crashtec.cdbprocessor import dbmodel
from crashtec.cdbprocessor import processor
from crashtec.cdbprocessor import resultparsers


import testconfig

TEST_DATA_FOLDER = 'test_data'
DUMP_FILE_NAME = os.path.join(os.path.dirname(__file__),
                                        TEST_DATA_FOLDER,
                                        "dump.dmp")

class Test01_CommandsHolder(unittest.TestCase):
    def test_positive_get_debugger_commands_for_task(self):
        task = Record()
        task[dbmodel.TASKS_PROBLEM_ID] =  infradefs.PROBLEMID_HANG
        commands_holder = processor.CdbCommandsHolder(testconfig)
        self.assertEqual(testconfig.HANG_COMMANDS_LIST,
                    commands_holder.get_debugger_commands_for_task(task),
                    "Wrong result for passed problem id"
                    )
        
    def test_negative_get_debugger_commands_for_task(self):
        task = Record()
        task[dbmodel.TASKS_PROBLEM_ID] = 'unknown_problem'
        commands_holder = processor.CdbCommandsHolder(testconfig)
        with self.assertRaises(CtBaseException):
                    commands_holder.get_debugger_commands_for_task(task)

class Test02_Debugger(unittest.TestCase):
    def test_positive_execute(self):
        debugger = processor.CdbDebugger(self.mock_config)
        task = Record()
        task[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        task[dbmodel.TASKS_DUMP_FILE_FIELD] = DUMP_FILE_NAME
        task[dbmodel.TASKS_SYMBOLS_PATH] = 'c:\\mock_path'
        result = debugger.execute(task, testconfig.HANG_COMMANDS_LIST)
        self.assertTrue(result, "Should not be empty")
    
    def test_negative_execute(self):
        debugger = processor.CdbDebugger(self.mock_config)
        task = Record()
        task[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        task[dbmodel.TASKS_DUMP_FILE_FIELD] = "z:\\unknown_dump.dmp"
        task[dbmodel.TASKS_SYMBOLS_PATH] = 'c:\\mock_path'
        with self.assertRaises(CtBaseException):
            debugger.execute(task, testconfig.HANG_COMMANDS_LIST)
    
    def setUp(self):
        self.mock_config = mock.MagicMock()
        self.mock_config.STANDARD_SYMBOLS_PATH = str()


_sample_task = {'id':1}
_sample_debugger_commnds = ['coommand1', 'command2']
_sample_debugger_output = 'sample output'
_sample_parsed_results = 'parsed_results'

class MockProcessorBuilder(object):
    def build_commands_holder(self):
        self.commands_holder = mock.create_autospec(
                            processor.CdbCommandsHolder(), spec_set = True)
        self.commands_holder.get_debugger_commands_for_task = MagicMock(
            return_value = _sample_debugger_commnds)
        return self
    
    def build_debugger(self):
        self.debugger =  mock.create_autospec(
                            processor.CdbDebugger(), spec_set = True) 
        self.debugger.execute = MagicMock(
            return_value = _sample_debugger_output)
        return self
    
    def build_parser(self):
        self.parser =  mock.create_autospec(
                            resultparsers.create_parser(), spec_set = True) 
        self.parser.parse_output = MagicMock(
                            return_value = _sample_parsed_results)
        return self
    
    def build_publisher(self):
        self.publisher =  mock.create_autospec(
                            processor.DbPublisher(), spec_set = True) 
        self.publisher.publish_results = MagicMock()
        return self
    
    def create(self):
        impl = processor.Implementation(self.commands_holder,
                                        self.debugger,
                                        self.parser,
                                        self.publisher)
        return processor.Processor('class_type', 'instance_name', 
                                   'group_id', impl)

class MockProcessorOneStepThrowsBuilder(MockProcessorBuilder):
    def build_publisher(self):
        self.publisher =  mock.create_autospec(
                            processor.DbPublisher(), spec_set = True) 
        self.publisher.publish_results = MagicMock(
                        side_effect = CtGeneralError('Mock intended error')) 
        return self
        
@patch('crashtec.infrastructure.public.agentbase.RegistrationHolder')
class Test03_Processor(unittest.TestCase): 
    # Here we should not have any errors. It is just regular success path.
    def test_task_success(self, mock_class):
        # Setup mock's
        processor_instance = self.create_mock_processor(MockProcessorBuilder())
        
        processor_instance.task_failed = MagicMock(side_effect = 
                                        RuntimeError("Should not be called"))
        
        # Call
        processor_instance.process_task(_sample_task)
        
        # Validate call's
        impl = processor_instance.impl 
        impl.commands_holder.get_debugger_commands_for_task.\
                        assert_called_once_with(_sample_task)
        impl.debugger.execute.\
                        assert_called_once_with(_sample_task,
                                                _sample_debugger_commnds)
        impl.parser.parse_output.\
                        assert_called_once_with(_sample_debugger_output)
        impl.publisher.publish_results.\
                        assert_called_once_with(_sample_task,
                                                _sample_parsed_results)
        processor_instance.task_finished.assert_called_once_with(_sample_task)
    
    def test_task_failed(self, mock_class):
        # Setup mock's
        processor_instance = self.create_mock_processor(
                                        MockProcessorOneStepThrowsBuilder())
        
        processor_instance.task_finished = MagicMock(side_effect = 
                                        RuntimeError("Should not be called"))
        
        # Call
        processor_instance.process_task(_sample_task)
        
        # Validate call's
        processor_instance.task_failed.assert_called_once_with(_sample_task)
    
    def create_mock_processor(self, builder):
        instance = builder.build_commands_holder().\
                    build_debugger().\
                    build_parser().\
                    build_publisher().\
                    create()
        instance.task_failed = MagicMock()
        instance.task_finished = MagicMock()
        return instance


def _get_sample_signature():
    return resultparsers.CrashSignature('problem_class', 
                                        'image_name', 
                                        'symbol_name', 
                                        'failure_bucket_id')

@patch('crashtec.db.provider.routines.create_new_record')
class Test04_DbPublisher(unittest.TestCase):
    def test_publish_results(self, mock_create_new_record):
        # Prepare samnple data
        task = Record()
        d = dbmodel
        task[PRIMARY_KEY_FIELD] = 212
        SAMPLE_DBG_OUTPUT = 'sample_output'
        
        # Call publisher
        publisher = processor.DbPublisher()
        r = resultparsers
        publisher.publish_results(task, [
                        r.CrashSignatureParserResults(_get_sample_signature()),
                        r.RawOutputParserResults(SAMPLE_DBG_OUTPUT)])
        
        # Validate publisher behavior
        s = _get_sample_signature()
        self.assertEqual(task[d.TASKS_PROBLEM_CLASS], s.problem_class)
        self.assertEqual(task[d.TASKS_SYMBOL_NAME], s.symbol_name)
        self.assertEqual(task[d.TASKS_FAIL_IMAGE], s.image_name)
        self.assertEqual(task[d.TASKS_FAILURE_BUCKET_ID], s.failure_bucket_id)
    
        new_record = Record()
        new_record[d.RAWRESULTS_TASK_ID] = 212
        new_record[d.RAWRESULTS_DBG_OUTPUT] = SAMPLE_DBG_OUTPUT
        mock_create_new_record.assert_called_once_with(d.RAWRESULTS_TABLE,
                                                       new_record)
           
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']e
    unittest.main()