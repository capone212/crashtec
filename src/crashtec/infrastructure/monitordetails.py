'''
Created on 28.02.2013

Implementation details of monitor

@author: capone
'''
import itertools
import collections
from crashtec.config import crashtecconfig
from crashtec.utils.exceptions import *
import logging

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


def get_next_agent_class(current_agent, task):
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

def get_combatable_agents_instances(task_record, class_type):
    pass
