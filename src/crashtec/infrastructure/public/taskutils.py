'''
Created on 17.02.2013

@author: capone
'''
from crashtec.infrastructure.dbmodel import *

TASK_STATUS_AGENT_FINISHED = 'agent_finished'
TASK_STATUS_AGENT_SCHEDULED = 'agent_scheduled'
TASK_STATUS_SUCCESS = 'success'
TASK_STATUS_FAILED = 'failed'

# Adjusts record values to mark task finished for specific agent.
# task_record record is instance of class Record
def mark_agent_finished(task_record, agent_class_name, agent_instance_name):
    task_record[TASKS_AGENT_CLASS_FIELD] = agent_class_name
    task_record[TASKS_AGENT_INSTANCE_FIELD] = agent_instance_name
    task_record[TASKS_STATUS_FIELD] = TASK_STATUS_AGENT_FINISHED