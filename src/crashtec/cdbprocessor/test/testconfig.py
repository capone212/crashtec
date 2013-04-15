'''
Created on 15.04.2013

@author: capone
'''
from crashtec.infrastructure.public import definitions
from crashtec.utils import windebuggers as wd

CRASH_COMMANDS_LIST = [wd.COMMAND_ANALYZE_V,
                       wd.COMMAND_LIST_THREADSTACKS, 
                       wd.COMMAND_QUIT
                      ]

HANG_COMMANDS_LIST = [
                       wd.COMMAND_LIST_THREADSTACKS, 
                       wd.COMMAND_QUIT
                      ]

COMMANDS_MAP = {
                    definitions.PROBLEMID_CRASH : CRASH_COMMANDS_LIST,
                    definitions.PROBLEMID_HANG : HANG_COMMANDS_LIST
                }