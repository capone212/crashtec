'''
Created on 17.02.2013

@author: capone
'''

TASK_STATUS_AGENT_FINISHED = 'agent_finished'

# Adjusts record values to mark task finished for specific agent.
def mark_agent_finished(task_record, agent_class_name, agent_instance_name):
    task_record.agent_class_type = agent_class_name
    task_record.agent_instance_name = agent_instance_name
    task_record.status = TASK_STATUS_AGENT_FINISHED