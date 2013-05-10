'''
Created on 18.02.2013

-
@author: anzor.apshev
'''
import logging
import time
import monitordetails
import definitions
from crashtec.infrastructure.public import agentbase
from crashtec.utils import exceptions as ctexceptions

_logger = logging.getLogger("infrastructure.monitor")

# FIXME: use timings info with agent instances to control alive clients  
class AgentsMonitor(object):
    def __init__(self, impl, instance_name, 
                 class_type = definitions.MONITOR_CLASS_TYPE):
        self.impl = impl
        self.register_holder = agentbase.RegistrationHolder(
                                            class_type, instance_name)
    
    def run(self):
        self.register_holder.start()
        #TODO: find out how to catch terminating signal for proper cleanup resources
        while (True):
            _logger.debug('fetching tasks for schedule...')
            tasks = self.impl.fetch_unscheduled_tasks()
            _logger.debug('fetched tasks: %s', tasks)
            for record in tasks:
                self.promote_task_progress(record)
            _logger.debug('One iteration done.')
            #TODO: use configurable settings here
            time.sleep(10)
        self.register_holder.stop_thread()
    
    def promote_task_progress(self, task_record):
        try:
            _logger.info("promoting task %s...", 
                         self.impl.get_task_id(task_record))
            next_agent_class = self.impl.get_next_agent_class(task_record)
            if not next_agent_class:
                # All agents finished their job
                _logger.debug('Marking task as finished: task_id = %s', 
                              self.impl.get_task_id(task_record))
                self.impl.set_task_finished(task_record)
                return
            _logger.info("next agent class for task %s is %s", 
                         self.impl.get_task_id(task_record), next_agent_class)
            # Select next agent for job
            compatible_agents = self.impl.get_compatible_agent_instances(
                                                next_agent_class, task_record)
            next_agent_record = self.impl.chose_best_agent_for_task(
                                                compatible_agents, task_record)
            if (not next_agent_record):
                # TODO: introduce postponed flag, according to time settings
                # there are no ready agents for this task
                _logger.warning("Can't promote task %s: "
                                "there is no compatible agents.",
                                self.impl.get_task_id(task_record))
                return
            
            _logger.info("next agent instance for task %s is %s",
                         self.impl.get_task_id(task_record), 
                         self.impl.get_agent_id(next_agent_record))
            
            self.impl.set_agent_for_task(next_agent_record, task_record)
        except ctexceptions.CtBaseException:
            self.impl.set_task_failed(task_record)
            _logger.error("Can't promote task %s:"
                          " internal error occurred during promoting", 
                          self.impl.get_task_id(task_record))

 
class AgentClassLocator(object):
    def get_next_agent_class(self, task_record):
        return monitordetails.get_next_agent_class(task_record)

class AgentsInstancesLocator(object):
    def get_compatible_agent_instances(self, class_type, task_record):
        return monitordetails.get_compatible_agent_instances(class_type, 
                                                             task_record)

class LoadBalancer(object):
    def chose_best_agent_for_task(self, agents_list, task_record):
        return monitordetails.chose_best_agent_for_task(agents_list, 
                                                        task_record)

class TasksStorageProvider(object):
    def fetch_unscheduled_tasks(self):
        return monitordetails.fetch_unscheduled_tasks()
    
    def set_task_finished(self, task_record):
        monitordetails.set_task_finished(task_record)
    
    def set_task_failed(self, task_record):
        monitordetails.set_task_failed(task_record)
    
    def set_agent_for_task(self, agent_record, task_record):
        return monitordetails.set_agent_for_task(agent_record, task_record) 

class Implementation(object):
    
    def __init__(self,
                  agents_class_locator = AgentClassLocator(),
                  agents_instances_locator = AgentsInstancesLocator(),
                  load_balancer = LoadBalancer(),
                  tasks_table = TasksStorageProvider()
                 ):
        self.agents_class_locator = agents_class_locator
        self.agents_instances_locator = agents_instances_locator
        self.load_balancer = load_balancer
        self.tasks_table = tasks_table
    
    # returns list of tasks needs status changing
    def fetch_unscheduled_tasks(self):
        return self.tasks_table.fetch_unscheduled_tasks()    
    
    # Returns next executor agents class
    def get_next_agent_class(self, task_record):
        return self.agents_class_locator.get_next_agent_class(task_record)
   
    # Returns list of compatible agents for the task
    def get_compatible_agent_instances(self, class_type, task_record):
        return self.agents_instances_locator.get_compatible_agent_instances(
                                                                class_type, 
                                                                task_record)
    
    def chose_best_agent_for_task(self, agents_list, task_record):
        return self.load_balancer.chose_best_agent_for_task(agents_list,
                                                             task_record)

    def set_agent_for_task(self, agent_record, task_record):
        return self.tasks_table.set_agent_for_task(agent_record, task_record)
    
    def set_task_finished(self, task_record):
        self.tasks_table.set_task_finished(task_record)
    
    def set_task_failed(self, task_record):
        self.tasks_table.set_task_failed(task_record)
    
    def get_task_id(self, task_record):
        return monitordetails.get_task_id(task_record)
    
    def get_agent_id(self, agent_record):
        return monitordetails.get_agent_id(agent_record)

