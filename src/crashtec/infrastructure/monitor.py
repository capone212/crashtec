'''
Created on 18.02.2013

- infinity loop
- fetch tasks with status 
-


@author: anzor.apshev
'''

from crashtec.db.provider.filter import FieldFilterFactory
from crashtec.db.provider import routines as dbroutines
from dbmodel import *
from public import taskutils


def main():
    #TODO: find out how to catch terminating signal for proper cleanup resources 
    
    while (True):
        f = FieldFilterFactory
        cursor = dbroutines.select_from(TASKS_TABLE,
                        filter = (f(STATUS_FIELD) == taskutils.TASK_STATUS_AGENT_FINISHED)
                    )
        print cursor.fetch_one()
        #TODO: replace with sleep
        return
        
main()