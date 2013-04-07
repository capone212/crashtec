'''
Created on 09.02.2013

@author: capone
'''
from crashtec.config import mooverconfig 
import dumpenumerator
from crashtec.db.provider import routines as dbroutines 
import shutil
import os.path
import definitions
from crashtec.utils import system as utilssystem
from crashtec.infrastructure.public import taskutils
import dbmodel
from crashtec.infrastructure.public import agentutils
from crashtec.infrastructure.public import definitions as infradefs

def enumerate_dump_files() :
    return dumpenumerator.get_input_dumps(mooverconfig.INPUT_DIR)
    
def move_dump_file(dump_file):
    #TODO: handle exceptions
    #TODO: replace this with actually move
    new_file_name = os.path.join(mooverconfig.DUMPS_DIR, os.path.basename(dump_file))
    shutil.move(dump_file, new_file_name)
    #update DB info
    new_task = dbroutines.Record()
    new_task[dbmodel.TASKS_DUMP_FILE_FIELD] = new_file_name
    new_task[dbmodel.TASKS_PROBLEM_ID] = infradefs.PROBLEMID_CRASH
    
    executor_instance_name = "%s@%s" % (
            definitions.AGENT_CLASS_TYPE, utilssystem.get_host_name())
    taskutils.mark_agent_finished(new_task, 
            definitions.AGENT_CLASS_TYPE, executor_instance_name)
    dbroutines.create_new_record(dbmodel.TASKS_TABLE, new_task)
    
def main():
    while (True):
        #TODO: add sleep here
        dump_files = enumerate_dump_files()
        for dump_file in dump_files:
            move_dump_file(dump_file)
        return

executor_instance_name = "%s@%s" % (
            definitions.AGENT_CLASS_TYPE, utilssystem.get_host_name())

agentutils.register_agent(executor_instance_name, definitions.AGENT_CLASS_TYPE)        
main()        
        