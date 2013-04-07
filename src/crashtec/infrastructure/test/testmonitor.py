'''
Created on 31.03.2013

@author: capone
'''

import unittest
import logging

from crashtec.infrastructure import monitor
from crashtec.infrastructure import dbmodel
from crashtec.config import crashtecconfig
from config import crashtectestconfig
from crashtec.db.provider import routines as dbroutines
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD
from crashtec.infrastructure.public import definitions as infradefs
from crashtec.utils.exceptions import CtBaseException

from crashtec.utils import debug

def setup_log():
    logger = logging.getLogger('infrastructure.monitor')
    debug.init_debug_logger(logger)

class Test01_AgentClassLocator(unittest.TestCase):        
    def test_simple_promoting(self):
        self.check_promote_task(crashtectestconfig.CRASHMOVER_CLASS, 
                                crashtectestconfig.CHECKER_CLASS)
    def test_branch_promoting(self):
        self.check_promote_task(crashtectestconfig.CHECKER_CLASS, 
                                crashtectestconfig.PROCESSOR_X86_CLASS)
    def test_last_agent(self):
        self.check_promote_task(crashtectestconfig.PROCESSOR_X86_CLASS, None)
    
    def test_invalid_agent(self):
        # Here we pass x64 processor agent to x86 task
        with self.assertRaises(CtBaseException):
            self.check_promote_task(crashtectestconfig.PROCESSOR_X64_CLASS,
                                    None)
        
    def check_promote_task(self, current_class, expected_next):
        locator = monitor.AgentClassLocator()
        record = dbroutines.Record()
        record[dbmodel.TASKS_AGENT_CLASS_FIELD] = current_class
        record[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        next_class = locator.get_next_agent_class(record)
        self.assertEqual(next_class, expected_next, 
                                        "Wrong next agent class!")
    
    @classmethod
    def setUpClass(cls):
        # FIXME: replace this odd thing with passing config modules
        # as parameters to agents
        cls.original_sequence =  crashtecconfig.JOB_SEQUENCE
        crashtecconfig.JOB_SEQUENCE = crashtectestconfig.TEST_JOB_SEQUENCE
    
    @classmethod
    def tearDownClass(cls):
        crashtecconfig.JOB_SEQUENCE = cls.original_sequence
    
class Test02_LoadBalancer(unittest.TestCase):
    def test_chose_best_agent_for_task(self):
        record = dbroutines.Record()
        agents_list = ['moover@agen1.cxm', 'moover2@agen2.cxm']
        load_balancer = monitor.LoadBalancer()
        agent_id = load_balancer.chose_best_agent_for_task(agents_list,
                                                            record)
        self.assertIn(agent_id, agents_list, 
                      "Retured agent is not in list")
    
    def test_empty_agents(self):
        record = dbroutines.Record()
        agents_list = []
        load_balancer = monitor.LoadBalancer()
        agent_id = load_balancer.chose_best_agent_for_task(agents_list,
                                                            record)
        self.assertIsNone(agent_id)


class TaskPromoteTestMock(object):
    def __init__(self, parent):
        self.agents_list = ['checker@agen1.cxm', 'checker@agen2.cxm']
        self.parent = parent
        self.task_promoted = False

    # Returns list of compatible agents for the task
    def get_compatible_agent_instances(self, class_type, task_record):
        result = []
        for agent_id in self.agents_list:
            record = dbroutines.Record()     
            record[dbmodel.AGENTS_INSTANCE_FIELD] = agent_id
            result.append(record)
        return result
    
    def set_agent_for_task(self, agent_record, task_record):
        self.parent.assertIn(agent_record[dbmodel.AGENTS_INSTANCE_FIELD],
                             self.agents_list, 
                             "Retured agent is not in list")
        self.task_promoted = True

    
    def set_task_finished(self, task_record):
        self.parent.fail("set_task_finished shouldn't be called")
    
    def set_task_failed(self, task_record):
        self.parent.fail("set_task_failed shouldn't be called")

class TaskFinishedTestMock(object):
    def __init__(self, parent):
        self.task_promoted = False

    def get_compatible_agent_instances(self, class_type, task_record):
        self.parent.fail("get_compatible_agent_instances"
                         "shouldn't be called")
    
    def set_agent_for_task(self, agent_record, task_record):
        self.parent.fail("set_agent_for_task shouldn't be called")
        
    def set_task_finished(self, task_record):
        self.task_promoted = True
    
    def set_task_failed(self, task_record):
        self.parent.fail("set_task_failed shouldn't be called")

class TaskFailedTestMock(object):
    def __init__(self, parent):
        self.task_promoted = False

    def get_compatible_agent_instances(self, class_type, task_record):
        self.parent.fail("get_compatible_agent_instances"
                         "shouldn't be called")
    
    def set_agent_for_task(self, agent_record, task_record):
        self.parent.fail("set_agent_for_task shouldn't be called")
        
    def set_task_finished(self, task_record):
        self.parent.fail("set_task_finished shouldn't be called")
    
    def set_task_failed(self, task_record):
        self.task_promoted = True


class TaskPostponedTestMock(object):
    def __init__(self, parent):
        self.task_promoted = False

    def get_compatible_agent_instances(self, class_type, task_record):
        return []
    
    def set_agent_for_task(self, agent_record, task_record):
        self.parent.fail("set_agent_for_task shouldn't be called")
        
    def set_task_finished(self, task_record):
        self.parent.fail("set_task_finished shouldn't be called")
    
    def set_task_failed(self, task_record):
        self.parent.fail("set_task_failed shouldn't be called")


#@unittest.skip("debug skipping")    
class Test03_AgentsMonitor(unittest.TestCase):
    "Checks assigning to task next agent instance"
    def test_task_promote(self):
        self.check_agents_monitor(crashtectestconfig.CRASHMOVER_CLASS,
                                   TaskPromoteTestMock(self))
    
    "Checks that monitor assign finished state after last agent" 
    "class in job sequence"
    def test_task_finished(self):
        self.check_agents_monitor(crashtectestconfig.PROCESSOR_X86_CLASS,
                                   TaskFinishedTestMock(self))
    
    "Checks that monitor assign finished state"
    "after last agent class in job sequence"
    def test_task_failed(self):
        self.check_agents_monitor(crashtectestconfig.PROCESSOR_X64_CLASS,
                                   TaskFailedTestMock(self))
    
    def check_agents_monitor(self, current_agent_class, mock_object):
        task_record = self.create_mock_task_record()
        task_record[dbmodel.TASKS_AGENT_CLASS_FIELD]  = current_agent_class
        impl = monitor.Implementation(tasks_table = mock_object,
                                agents_instances_locator = mock_object)
        agents_monitor = monitor.AgentsMonitor(impl)
        agents_monitor.promote_task_progress(task_record)
        self.assertTrue(mock_object.task_promoted, 
                        'Task was not promoted')
    
    def create_mock_task_record(self):
        task_record = dbroutines.Record()
        task_record[PRIMARY_KEY_FIELD] = '1'
        task_record[dbmodel.TASKS_PLATFORM_FIELD] = infradefs.PLATFORM_WIN32
        return task_record
    
    @classmethod
    def setUpClass(cls):
        cls.original_sequence =  crashtecconfig.JOB_SEQUENCE
        crashtecconfig.JOB_SEQUENCE = crashtectestconfig.TEST_JOB_SEQUENCE
    
    @classmethod
    def tearDownClass(cls):
        crashtecconfig.JOB_SEQUENCE = cls.original_sequence


setup_log()