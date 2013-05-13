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
from crashtec.infrastructure.public import taskutils
 

import dbmodel
import resultspublisher
import resultparsers

_logger = logging.getLogger("cdb_processor")

class Processor(agentbase.AgentBase):
    '''
    Processor does the main task for analyzing crash reports. It runs
    cdb.exe (windows debugger) against a memory dump and parses the response.    
    ''' 
    def __init__(self, class_type, instance_name, group_id, impl):
        '''
        Constructor.
        
        Parameters
        class_type - agent class id, see definitions module for possible values.
        instance_name - system wide unique id of agent instance. 
                        See parent class for more details.
        impl - provides implementation details for each step of processor
        '''
        agentbase.AgentBase.__init__(self, class_type, instance_name, group_id)
        self.impl = impl
    
    
    def process_task(self, task):
        try:
            _logger.info('Start processing new task is = %s', 
                         taskutils.get_task_id(task))
            comands_list = self.impl.get_debugger_commands_for_task(task)
            debugger_output = self.impl.exec_debugger(task, comands_list)
            parsed_results = self.impl.parse_output(debugger_output)
            self.impl.publish_results(task, parsed_results)
            _logger.info('Finished processing task id is = %s', 
                         taskutils.get_task_id(task))
            self.task_finished(task)
        except CtBaseException as e:
            _logger.error('Exception occurred while processing task: %s', e)
            self.task_failed(task)

class Implementation(object):
    '''
    Hides implementation details of Processor class.
    
    Uses Template Method and Delegation design patterns to easily 
    vary algorithm steps. 
    '''
    
    def __init__(self, commands_holder, debugger, output_parser, publisher):
        '''
            Constructor
            
            Input parameters are delegate objects that responsible for 
            executing single algorithm step.
            
        '''
        self.commands_holder = commands_holder
        self.debugger = debugger
        self.parser = output_parser
        self.publisher = publisher
        
    def get_debugger_commands_for_task(self, task):
        '''Returns list of debugger commands_holder for current task'''
        return self.commands_holder.get_debugger_commands_for_task(task)
    
  
    def exec_debugger(self, task, command_list):
        '''Returns raw output of debugger. 
        
        It should be up to several kb sized string.
        '''
        return self.debugger.execute(task, command_list)
     
    def parse_output(self, debugger_output):
        '''Returns iteratable container of parsed visitable results.'''
        return self.parser.parse_output(debugger_output)
      
    def publish_results(self, task, parsed_results):
        '''Saves processing results into DB.'''
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
    
    def __init__(self, config = processorconfig):
        self.config = config
    
    def execute(self, task, command_list):
        image_path = str()
        symbols_path = self.config.STANDARD_SYMBOLS_PATH
        if (task[dbmodel.TASKS_SYMBOLS_PATH]):
            image_path = task[dbmodel.TASKS_SYMBOLS_PATH] 
            symbols_path = "%s;%s" % (symbols_path, 
                                      task[dbmodel.TASKS_SYMBOLS_PATH])
        print image_path
        print symbols_path
        return windebuggers.exec_cdb(command_list,
                                     task[dbmodel.TASKS_PLATFORM_FIELD],
                                     task[dbmodel.TASKS_DUMP_FILE_FIELD],
                                     image_path,
                                     symbols_path)

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

            