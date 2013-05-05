'''
Created on 09.02.2013

@author: capone
'''
from crashtec.config import moverconfig 
import dumpenumerator
from crashtec.db.provider import routines as dbroutines 
import shutil
import os.path
import time
import definitions
from crashtec.utils import system as utilssystem
from crashtec.infrastructure.public import taskutils
import dbmodel
from crashtec.infrastructure.public import agentbase
from crashtec.infrastructure.public import definitions as infradefs

import logging

_logger = logging.getLogger("crashtec.mover")

# FIXME: create unique place for dump file
class Mover(object):
    def __init__(self, class_type, instance_name):
        self.class_type = class_type
        self.instance_name = instance_name
        self.register_holder = agentbase.RegistrationHolder(
                                            class_type, instance_name)
        
    def move_dump_file(self, dump_file):
        #TODO: handle exceptions
        #TODO: replace this with actually move
        new_file_name = os.path.join(moverconfig.DUMPS_DIR,
                                      os.path.basename(dump_file))
        shutil.move(dump_file, new_file_name)
        #update DB info
        new_task = dbroutines.Record()
        new_task[dbmodel.TASKS_DUMP_FILE_FIELD] = new_file_name
        new_task[dbmodel.TASKS_PROBLEM_ID] = infradefs.PROBLEMID_CRASH
        
        default_instance_name = "%s@%s" % (
                definitions.AGENT_CLASS_TYPE, utilssystem.get_host_name())
        taskutils.mark_agent_finished(new_task, 
                definitions.AGENT_CLASS_TYPE, default_instance_name)
        dbroutines.create_new_record(dbmodel.TASKS_TABLE, new_task)
    
    def enumerate_dump_files(self) :
        return dumpenumerator.get_input_dumps(moverconfig.INPUT_DIR)
    
    def run(self):
        while (True):
            #TODO: add sleep here
            dump_files = self.enumerate_dump_files()
            for dump_file in dump_files:
                _logger.info('Moving new dump file %s', dump_file)
                self.move_dump_file(dump_file)
            time.sleep(10)      
        