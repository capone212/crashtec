'''
Created on 06.04.2013

@author: capone
'''
import monitor
from crashtec.utils import debug as ctdebug

def run_monitor():
    ctdebug.init_debug_logger(monitor._logger)
    default_implementation = monitor.Implementation()
    monitor_instance = monitor.AgentsMonitor(default_implementation)
    monitor_instance.run()

if __name__ == '__main__':
    run_monitor()