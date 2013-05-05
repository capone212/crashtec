'''
Created on 22.02.2013

@author: anzor.apshev
'''
import logging

from crashtec.infrastructure.public import agentbase
from crashtec.infrastructure.public import taskutils
from crashtec.utils.exceptions import CtBaseException

import definitions
import checkerdetails
import dbmodel

_logger = logging.getLogger("checker.checkerdeamon")


class Implementation(object):
    # Returns text output of dump checker tool. Throws exceptions on error. 
    def execute_dump_checker(self, dump_file_name):
        return checkerdetails.execute_dump_checker(dump_file_name)
    
    # Returns map of parsed parameters. Throws exceptions on error. 
    def parse_checker_output(self, checker_output):
        return checkerdetails.parse_checker_output(checker_output)

# TODO: write unit tests
class Checker(agentbase.AgentBase):
    def __init__(self, impl, instance_name, 
                 class_type=definitions.AGENT_CLASS_TYPE):
        self.impl = impl
        agentbase.AgentBase.__init__(self, class_type, instance_name)
    
    def process_task(self, task):
        _logger.debug('About to start processing task: %s',  task)
        try:
            checker_output = self.impl.execute_dump_checker(
                                task[dbmodel.TASKS_DUMP_FILE_FIELD])
            params_map = self.impl.parse_checker_output(checker_output)
            taskutils.set_platform_for_task(task, 
                                        params_map[definitions.PLATFORM_PARAM])
            self.task_finished(task)
            _logger.debug('Task finished')
        except CtBaseException as e:
            _logger.error('Exception occurred while checking dump: %s', e)
            self.task_failed(task)

        