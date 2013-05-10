'''
Created on 17.02.2013

@author: capone
'''
from crashtec.infrastructure import dbmodel

from agentutils import GROUP_ID_UNSET

from crashtec.db.provider.routines import Record as DbRecord

TASK_STATUS_AGENT_FINISHED = 'agent_finished'
TASK_STATUS_AGENT_SCHEDULED = 'agent_scheduled'
TASK_STATUS_SUCCESS = 'success'
TASK_STATUS_FAILED = 'failed'

# Adjusts record values to mark task finished for specific agent.
# task_record record is instance of class Record
def mark_agent_finished(task_record):
    task_record[dbmodel.TASKS_STATUS_FIELD] = TASK_STATUS_AGENT_FINISHED
    
def mark_agent_failed(task_record):
    task_record[dbmodel.TASKS_STATUS_FIELD] = TASK_STATUS_FAILED
    

def set_agent_for_task(task_record, agent_class_name, 
                       agent_instance_name, group_id=GROUP_ID_UNSET):
    d = dbmodel
    task_record[d.TASKS_AGENT_CLASS_FIELD] = agent_class_name
    task_record[d.TASKS_AGENT_INSTANCE_FIELD] = agent_instance_name
    if (group_id != GROUP_ID_UNSET):
        task_record[d.TASKS_AGENTS_GROUP_ID] = group_id
    
def set_platform_for_task(task_record, platform):
    task_record[dbmodel.TASKS_PLATFORM_FIELD] = platform

def new_task_record():
    new_task = DbRecord()
    new_task[dbmodel.TASKS_AGENTS_GROUP_ID] = GROUP_ID_UNSET
    return new_task
    