'''
Created on 18.02.2013

- infinity loop
- fetch tasks with status 
-
@author: anzor.apshev
'''
import itertools
import logging
import collections
from crashtec.db.provider.filter import FieldFilterFactory
from crashtec.db.provider import routines as dbroutines
from crashtec.config import crashtecconfig
from dbmodel import *
from public import taskutils
from crashtec.utils.exceptions import *

_logger = logging.getLogger("infrastructure.monitor")

def iterate_over(job_sequence, task):
    for entry in job_sequence:
        element_value = entry.value(task)
        if not element_value:
            continue
        if isinstance(element_value, collections.Iterable) and not isinstance(element_value, basestring):
            for sub in iterate_over(element_value, task):
                yield sub
        else:
            yield element_value

#
#task = {'platform' : 'linux'}
#for x in iterate_over(sequence, task):
#    print x

def get_next_agent_class(current_agent, task):
    #ambda x: x**2
    iter = itertools.dropwhile(lambda x: x != current_agent,
                               iterate_over(crashtecconfig.JOB_SEQUENCE, task))
    # locate current element in JOB_SEQUENCE                           )
    try:
        iter.next()
    except StopIteration:
        _logger.error("Can't find current agent in a sequence. Current cgent_class %s" % current_agent)
        raise GeneralError()
    # advance to next agent 
    try:
        return iter.next()
    except StopIteration:
        # this means that current agent is the last in the job sequence
        return None
        
        
def promote_task_progress(task_record):
    try:
        next_agent_class = get_next_agent_class(
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
    
    
def main():
    #TODO: find out how to catch terminating signal for proper cleanup resources 
    while (True):
        f = FieldFilterFactory
        cursor = dbroutines.select_from(TASKS_TABLE,
                        filter = (f(TASKS_STATUS_FIELD) == taskutils.TASK_STATUS_AGENT_FINISHED)
                    )
        record = cursor.fetch_one()
        promote_task_progress(record)
        #TODO: replace with sleep
        return
        
main()