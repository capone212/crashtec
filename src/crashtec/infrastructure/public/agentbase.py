'''
Created on 07.03.2013

@author: capone
'''

import threading
from crashtec.infrastructure.public import agentutils
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilter
from crashtec.infrastructure import dbmodel
from  crashtec.db.schema import fields
import taskutils
import time

class RegistrationHolder(threading.Thread):
    def __init__(self, class_type, instance_name):
        agentutils.register_agent(class_type, instance_name)
        self.m_stop_event = threading.Event()
        self.instance_name = instance_name
        threading.Thread.__init__(self)
    
    def stop_thread(self):
        self.m_stop_event.set()
        self.join()
    
    def run(self):
        while (not self.m_stop_event.is_set()):
            agentutils.send_keepalive_message(self.instance_name)
            self.m_stop_event.wait(5)   

class AgentBase(object):
    def __init__(self, class_type, instance_name):
        self.class_type = class_type
        self.instance_name = instance_name 
        self.m_register_holder = RegistrationHolder(class_type, instance_name)
    
    def run(self):
        while (True):
            task = self.fetch_task()
            if (not task) :
                #TODO: use configurable settings here
                time.sleep(5)
                continue
            self.process_task(task)
        
    def process_task(self, task):
        raise  RuntimeError("This function should be delegated to derived class impl")
            
    
    def fetch_task(self):
        d = dbmodel
        f = dbfilter.FieldFilterFactory
        session = dbroutines.select_from(d.TASKS_TABLE, filter = (
            (f(d.TASKS_AGENT_INSTANCE_FIELD) == self.instance_name) &
            (f(d.TASKS_STATUS_FIELD) == taskutils.TASK_STATUS_AGENT_SCHEDULED)),
            order = dbfilter.Ascent(fields.PRIMARY_KEY_FIELD))
        #Think about fetching fixed amount of tasks
        return session.fetch_one()
        