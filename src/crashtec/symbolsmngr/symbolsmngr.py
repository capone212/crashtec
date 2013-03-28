'''
Created on 15.03.2013

@author: capone
'''
import logging

from crashtec.infrastructure.public import agentbase
from crashtec.infrastructure.public import taskutils
from crashtec.utils.exceptions import CtBaseException

import definitions
import dbmodel

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

# TODO: So, use dependency injection pattern here. And read about it first... :)
    
class SymbolsManager(agentbase.AgentBase):
    def __init__(self, products_detector, class_type, instance_name):
        self.products_detector = products_detector
        agentbase.AgentBase.__init__(self, class_type, instance_name)
    
    def process_task(self, task):
        _logger.debug('About to start processing task: %s',  task)
        try:
            products_list = self.products_detector.get_products_list_for_task(task)
            self.task_finished(task)
        except CtBaseException as e:
            _logger.error('Exception occurred while checking dump: %s', e)
            self.task_failed(task)