'''
Created on 15.04.2013

@author: capone
'''
import unittest
import os

from crashtec.utils.exceptions import CtBaseException
from crashtec.db.provider.routines import Record
from crashtec.infrastructure.public import definitions as infradefs

from crashtec.cdbprocessor import dbmodel
from crashtec.cdbprocessor import processor

import testconfig

TEST_DATA_FOLDER = 'test_data'
DUMP_FILE_NAME = os.path.join(os.path.dirname(__file__),
                                        TEST_DATA_FOLDER,
                                        "dump.dmp")

class Test01_CommandsHolder(unittest.TestCase):
    def test_positive_get_debugger_commands_for_task(self):
        task = Record()
        task[dbmodel.TASKS_PROBLEM_ID] =  infradefs.PROBLEMID_HANG
        commands_holder = processor.CommandsHolder(testconfig)
        self.assertEqual(testconfig.HANG_COMMANDS_LIST,
                    commands_holder.get_debugger_commands_for_task(task),
                    "Wrong result for passed problem id"
                    )
        
    def test_negative_get_debugger_commands_for_task(self):
        task = Record()
        task[dbmodel.TASKS_PROBLEM_ID] = 'unknown_problem'
        commands_holder = processor.CommandsHolder(testconfig)
        with self.assertRaises(CtBaseException):
                    commands_holder.get_debugger_commands_for_task(task)

class Test02_Debugger(unittest.TestCase):
    def test_positive_execute(self):
        debugger = processor.Debugger()
        task = Record()
        task[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        task[dbmodel.TASKS_DUMP_FILE_FIELD] = DUMP_FILE_NAME
        result = debugger.execute(task, testconfig.HANG_COMMANDS_LIST)
        self.assertTrue(result, "Should not be empty")
    
    def test_negative_execute(self):
        debugger = processor.Debugger()
        task = Record()
        task[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        task[dbmodel.TASKS_DUMP_FILE_FIELD] = "z:\\unknown_dump.dmp"
        with self.assertRaises(CtBaseException):
            debugger.execute(task, testconfig.HANG_COMMANDS_LIST)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']e
    unittest.main()