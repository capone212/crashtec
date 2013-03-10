'''
Created on 22.02.2013

@author: anzor.apshev
'''

import definitions
from crashtec.infrastructure.public import agentbase 

class Checker(agentbase.AgentBase):
    def __init__(self, class_type, instance_name):
        agentbase.AgentBase.__init__(self, class_type, instance_name)
    
    def process_task(self, task):
        print 'should be processed task ',  task
        

checker = Checker(definitions.EXECUTOR_CLASS_NAME, 'simple_checker')        
checker.run()

print "exit"
        