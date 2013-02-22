'''
Created on 22.02.2013

@author: anzor.apshev
'''
import threading
from crashtec.infrastructure.public import agentutils

# use Event for signaling stop or start of work
class AgentRegister(object):
    #TODO: place register_agent here
    #    start thread and update registration every 5 seconds

class AgentBase(object):
    def __init__(self, class_type, instance_name):
        agentutils.register_agent(class_type, instance_name)
        