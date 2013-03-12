'''
Created on 22.02.2013

@author: anzor.apshev
'''

import definitions
from crashtec.infrastructure.public import agentbase
import checkerdetails
from crashtec.utils.exceptions import CtBaseException
import logging


_logger = logging.getLogger("checker.checkerdeamon")

class implementation(object):
    # Throws exceptions on error. 
    # Returns text output of tool. 
    def execute_dump_checker(self, dump_file_name):
        return checkerdetails.execute_dump_checker(dump_file_name)

class Checker(agentbase.AgentBase):
    def __init__(self, impl, class_type, instance_name):
        self.impl = impl
        agentbase.AgentBase.__init__(self, class_type, instance_name)
    
    def process_task(self, task):
        print 'should be processed task ',  task
        try:
            pass
        except CtBaseException as e:
            _logger.error('Exception occurred while testing ')
        

checker = Checker(implementation(), definitions.EXECUTOR_CLASS_NAME, 'simple_checker')
checker.run()

print "exit"
        