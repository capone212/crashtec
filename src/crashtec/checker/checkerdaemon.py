'''
Created on 22.02.2013

@author: anzor.apshev
'''
import threading
from crashtec.infrastructure.public import agentutils

class RegistrationHolder(threading.Thread):
    def __init__(self, class_type, instance_name):
        agentutils.register_agent(class_type, instance_name)
        self.m_stop_event = threading.Event()
        self.instance_name = instance_name
        threading.Thread.__init__(self)
    
    def stop_thread(self):
        self.m_stop_event.set()
    
    def run(self):
        while (not self.m_stop_event.is_set()):
            agentutils.send_keepalive_message(self.instance_name)
            self.m_stop_event.wait(5)
            

class AgentBase(object):
    def __init__(self, class_type, instance_name):
        self.m_register_holder = RegistrationHolder(class_type, instance_name)
        
        

print "exit"
        