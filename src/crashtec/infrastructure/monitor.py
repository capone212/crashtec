'''
Created on 18.02.2013

- infinity loop
- fetch tasks with status 
-
@author: anzor.apshev
'''
import logging
from crashtec.db.provider.filter import FieldFilterFactory
from crashtec.db.provider import routines as dbroutines
from dbmodel import *
from public import taskutils
import monitordetails


_logger = logging.getLogger("infrastructure.monitor")

class AgentsMonitor(object):
    def __init__(self, impl):
        self.impl = impl
    
    def run(self):
        #TODO: find out how to catch terminating signal for proper cleanup resources 
        while (True):
            f = FieldFilterFactory
            cursor = dbroutines.select_from(TASKS_TABLE,
                            filter = (f(TASKS_STATUS_FIELD) == taskutils.TASK_STATUS_AGENT_FINISHED)
                        )
            record = cursor.fetch_one()
            self._promote_task_progress(record)
            #TODO: replace with sleep
            return
    
    def _promote_task_progress(self, task_record):
        try:
            next_agent_class = self.impl.get_next_agent_class(
                            task_record[TASKS_AGENT_CLASS_FIELD], task_record)
            if not next_agent_class:
                # All agents finished their job
                task_record[TASKS_STATUS_FIELD] = taskutils.TASK_STATUS_SUCCESS
                return task_record
            # Select next agent for job
            ## TODO:-------------------
        except BaseException:
            #TODO: set status to failed
            pass

# TODO: make factory for this class, that will construct this class according
# current application settings 
class Implementation(object):
    # Returns next executor agents class
    def get_next_agent_class(self, current_agent_class, record):
        return monitordetails.get_next_agent_class(current_agent_class, record)
    
    
default_implementation = Implementation()
_monitor = AgentsMonitor(default_implementation)
_monitor.run()
 