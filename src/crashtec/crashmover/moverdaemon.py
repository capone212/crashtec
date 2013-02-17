'''
Created on 09.02.2013

@author: capone
'''
from crashtec.config import mooverconfig 
import dumpenumerator
from crashtec.db.provider import operations as dboperations
import shutil
import os.path
import definitions
from crashtec.utils import system as utilssystem
from crashtec.infrastructure.public import taskutils

def enumerate_dump_files() :
    return dumpenumerator.get_input_dumps(mooverconfig.INPUT_DIR)
    
def move_dump_file(dump_file):
    #TODO: handle exceptions
    #TODO: replace this with actually move
    new_file_name = os.path.join(mooverconfig.DUMPS_DIR, os.path.basename(dump_file))
    shutil.move(dump_file, new_file_name)
    #update DB info
    new_task = dboperations.Record()
    new_task.dump_file_name = dump_file
    executor_instance_name = "%s@%s" % (
            definitions.EXECUTOR_CLASS_NAME, utilssystem.get_host_name())
    taskutils.mark_agent_finished(new_task, 
            definitions.EXECUTOR_CLASS_NAME, executor_instance_name)
    dboperations.create_new_record('tasks', new_task)
    
def main():
    while (True):
        #TODO: add sleep here
        dump_files = enumerate_dump_files()
        for dump_file in dump_files:
            move_dump_file(dump_file)
        return
        
main()        
        