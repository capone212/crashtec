'''
Created on 28.02.2013

Implementation details of monitor

@author: capone
'''
import itertools
import random
import collections
import logging
import datetime

from crashtec.config import crashtecconfig
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilter
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD
from crashtec.utils import exceptions as ctexceptions
from crashtec.infrastructure.public import agentutils

from public import taskutils
from public.jobsequence import GetJobEntryValueVisitor

import dbmodel

_logger = logging.getLogger("infrastructure.monitor")


def iterate_over(job_sequence, task):
    for entry in job_sequence:
        element_value = entry.accept(GetJobEntryValueVisitor(task))
        if not element_value:
            continue
        if (isinstance(element_value, collections.Iterable) and 
                        not isinstance(element_value, basestring)):
            for sub in iterate_over(element_value, task):
                yield sub
        else:
            yield element_value


def get_next_agent_class(task):
    current_agent = task[dbmodel.TASKS_AGENT_CLASS_FIELD]
    iterator = itertools.dropwhile(lambda x: x != current_agent,
                            iterate_over(crashtecconfig.JOB_SEQUENCE, task))
    # locate current element in JOB_SEQUENCE
    try:
        iterator.next()
    except StopIteration:
        _logger.error("Can't find current agent in a sequence." \
                      " Current agent_class %s" % current_agent)
        raise ctexceptions.CtGeneralError()
    # advance to next agent 
    try:
        return iterator.next()
    except StopIteration:
        # this means that current agent is the last in the job sequence
        return None

def _get_agents_last_keepalive_boundary():
    return datetime.datetime.now() - datetime.timedelta(
                    seconds=2*crashtecconfig.AGENTS_KEEPALIVE_TIMEOUT)

def get_compatible_agent_instances(class_type, task_record):
    f = dbfilter.FieldFilterFactory
    d = dbmodel
    filter_object = (f(d.AGENTS_CLASS_TYPE_FIELD) == class_type) & \
        (f(d.AGENTS_KEEPALIVE_FIELD) > _get_agents_last_keepalive_boundary())
    # Filter agents by group id, if necessary     
    if (task_record[d.TASKS_AGENTS_GROUP_ID] != agentutils.GROUP_ID_UNSET):
        filter_object = filter_object & (f(d.AGENTS_GROUP_FIELD) == \
                                         task_record[d.TASKS_AGENTS_GROUP_ID])
    
    cursor = dbroutines.select_from(d.AGENTS_TABLE, db_filter=filter_object)
    result = cursor.fetch_all()
    return result 

def chose_best_agent_for_task(agents_list, task):
    if not agents_list:
        return None
    return random.choice(agents_list)

def set_agent_for_task(agent_record, task_record):
    d = dbmodel
    taskutils.set_agent_for_task(task_record, 
                                 agent_record[d.AGENTS_CLASS_TYPE_FIELD], 
                                 agent_record[d.AGENTS_INSTANCE_FIELD], 
                                 agent_record[d.AGENTS_GROUP_FIELD])
    task_record[d.TASKS_STATUS_FIELD] = taskutils.TASK_STATUS_AGENT_SCHEDULED
    dbroutines.update_record(d.TASKS_TABLE, task_record)
    
def fetch_unscheduled_tasks():
    f = dbfilter.FieldFilterFactory
    d = dbmodel 
    cursor = dbroutines.select_from(d.TASKS_TABLE,
                            db_filter = (f(d.TASKS_STATUS_FIELD) == 
                                      taskutils.TASK_STATUS_AGENT_FINISHED)
                        )
    return cursor.fetch_all()
    
def set_task_finished(task_record):
    task_record[dbmodel.TASKS_STATUS_FIELD] = taskutils.TASK_STATUS_SUCCESS
    dbroutines.update_record(dbmodel.TASKS_TABLE, task_record)
    
def set_task_failed(task_record):
    task_record[dbmodel.TASKS_STATUS_FIELD] = taskutils.TASK_STATUS_FAILED
    dbroutines.update_record(dbmodel.TASKS_TABLE, task_record)

def get_task_id(task_record):
    return task_record[PRIMARY_KEY_FIELD]

def get_agent_id(agent_record):
    return agent_record[dbmodel.AGENTS_INSTANCE_FIELD]