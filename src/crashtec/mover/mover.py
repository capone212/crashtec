'''
Created on 09.02.2013

@author: capone
'''

import uuid 

from crashtec.config import moverconfig 
import dumpenumerator
from crashtec.db.provider import routines as dbroutines 
import shutil
import os.path
import time
from crashtec.infrastructure.public import taskutils
import dbmodel
from crashtec.infrastructure.public import agentbase
from crashtec.infrastructure.public import definitions as infradefs

import logging

_logger = logging.getLogger("crashtec.mover")

# TODO: write unit test on it

class UniquePathGenerator(object):
    
    '''
        Delegate object for generating unique ID for dump file.
        
        This id will used for creating directory for dump file in store, 
        so it should not contain any special characters. 
    '''

    def get_place_for_file(self, dump_file):
        # TODO: Generate id for file using SHA1, it will allow detect duplicating 
        # dump files.
        return os.path.join(moverconfig.DUMPS_DIR, 
                            str(uuid.uuid4()).replace('-', os.sep),
                            os.path.basename(dump_file))


class Mover(object):
    def __init__(self, class_type, instance_name,
                 path_generator = UniquePathGenerator()):
        self.class_type = class_type
        self.instance_name = instance_name
        self.path_generator = path_generator
        self.register_holder = agentbase.RegistrationHolder(
                                            class_type, instance_name)
        
    def move_dump_file(self, dump_file):
        #TODO: handle exceptions
        #TODO: replace this with actually move
        new_file_name = self.path_generator.get_place_for_file(dump_file)
        os.makedirs(os.path.dirname(new_file_name))
        shutil.move(dump_file, new_file_name)
        #update DB info
        new_task = taskutils.new_task_record()
        new_task[dbmodel.TASKS_DUMP_FILE_FIELD] = new_file_name
        new_task[dbmodel.TASKS_PROBLEM_ID] = infradefs.PROBLEMID_CRASH
        
        taskutils.set_agent_for_task(new_task, 
                                     self.class_type, 
                                     self.instance_name)
        taskutils.mark_agent_finished(new_task)
        dbroutines.create_new_record(dbmodel.TASKS_TABLE, new_task)
    
    def enumerate_dump_files(self) :
        return dumpenumerator.get_input_dumps(moverconfig.INPUT_DIR)
    
    def run(self):
        self.register_holder.start()
        while (True):
            dump_files = self.enumerate_dump_files()
            for dump_file in dump_files:
                _logger.info('Moving new dump file %s', dump_file)
                self.move_dump_file(dump_file)
            #TODO: use common setting here
            time.sleep(10)
        self.register_holder.stop_thread()
        