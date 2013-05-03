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

_logger = logging.getLogger("cdb_processor")

# FIXME: read about documenting of python code

class Processor(agentbase.AgentBase):
    '''
    Processor does a main task for analyzing crash reports. It runs
    cdb.exe (windows debugger) against a memory dump and parses a response.    
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
            result = self.exec_debugger(task, comands_list)

        except CtBaseException as e:
            _logger.error('Exception occurred while processing task: %s', e)
            self.task_failed(task)

class Implementation(object):
    def __init__(self, commands, debugger):
        self.commands = commands
        self.debugger = debugger
    
    # Returns list of debugger commands         
    def get_debugger_commands_for_task(self, task):
        return self.commands.get_debugger_commands_for_task(task)
    
    # Returns raw output of debugger. 
    # It should be up to several kb sized string.
    def exec_debugger(self, task, command_list):
        return self.debugger.exec_debugger(task, command_list)
    
    # Returns iteratable container of parsed results 
    def parse_output(self, debugger_output):
        pass
    

class CommandsHolder(object):
    def __init__(self, config = processorconfig):
        self.commands_map = config.COMMANDS_MAP
    
    def get_debugger_commands_for_task(self, task):
        d = dbmodel
        problem_id = task[d.TASKS_PROBLEM_ID]
        if not problem_id in self.commands_map:
            raise CtGeneralError("Can't find commands for problem_id %s" % \
                                 problem_id)
        return self.commands_map[problem_id]
    

class Debugger(object):
    def execute(self, task, command_list):
        return windebuggers.exec_cdb(command_list,
                                     task[dbmodel.TASKS_PLATFORM_FIELD],
                                     task[dbmodel.TASKS_DUMP_FILE_FIELD])


#TODO: write parsers that expose data structures, use visitor pattern to process it later
# Probably it better to use it abstract algh list  
            