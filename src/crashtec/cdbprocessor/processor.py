'''
Created on 06.04.2013

@author: capone

'''
import logging

from crashtec.infrastructure.public import agentbase
from crashtec.config import processorconfig
from crashtec.utils.exceptions import CtGeneralError
from crashtec.utils.exceptions import CtBaseException
from crashtec.utils import windebuggers
 

import dbmodel
import resultspublisher
import resultparsers

_logger = logging.getLogger("cdb_processor")

# FIXME: read about documenting of python code

class Processor(agentbase.AgentBase):
    '''
    Processor does a main task for analyzing crash reports. It runs
    cdb.exe (windows debugger) against a memory dump and parses the response.    
    ''' 
    def __init__(self, class_type, instance_name, impl):
        '''
        Constructor.
        impl - provides implementation details for each step of processor
        '''
        agentbase.AgentBase.__init__(self, class_type, instance_name)
        self.impl = impl
    
    
    def process_task(self, task):
        try:
            comands_list = self.impl.get_debugger_commands_for_task(task)
            debugger_output = self.impl.exec_debugger(task, comands_list)
            parsed_results = self.impl.parse_output(debugger_output)
            self.impl.publish_results(task, parsed_results)
            self.task_finished(task)
        except CtBaseException as e:
            _logger.error('Exception occurred while processing task: %s', e)
            self.task_failed(task)

class Implementation(object):
    def __init__(self, commands_holder, debugger, output_parser, publisher):
        self.commands_holder = commands_holder
        self.debugger = debugger
        self.parser = output_parser
        self.publisher = publisher
    
    # Returns list of debugger commands_holder for current task    
    def get_debugger_commands_for_task(self, task):
        return self.commands_holder.get_debugger_commands_for_task(task)
    
    # Returns raw output of debugger. 
    # It should be up to several kb sized string.
    def exec_debugger(self, task, command_list):
        return self.debugger.execute(task, command_list)
    
    # Returns iteratable container of parsed visitable results. 
    def parse_output(self, debugger_output):
        return self.parser.parse_output(debugger_output)
    
    # Saves processing results into DB.  
    def publish_results(self, task, parsed_results):
        self.publisher.publish_results(task, parsed_results)
    

class CdbCommandsHolder(object):
    def __init__(self, config = processorconfig):
        self.commands_map = config.COMMANDS_MAP
    
    def get_debugger_commands_for_task(self, task):
        d = dbmodel
        problem_id = task[d.TASKS_PROBLEM_ID]
        if not problem_id in self.commands_map:
            raise CtGeneralError("Can't find commands_holder for problem_id %s" % \
                                 problem_id)
        return self.commands_map[problem_id]
    

class CdbDebugger(object):
    def execute(self, task, command_list):
        return windebuggers.exec_cdb(command_list,
                                     task[dbmodel.TASKS_PLATFORM_FIELD],
                                     task[dbmodel.TASKS_DUMP_FILE_FIELD])

class DbPublisher():
    def publish_results(self, task, parsed_results):
        visitor = resultspublisher.ResultsPublisher(task)
        for result_item in parsed_results:
            result_item.accept(visitor)

def create_default_implementation():
    return Implementation(CdbCommandsHolder(), 
                          CdbDebugger(), 
                          resultparsers.create_parser(),
                          DbPublisher())

            