'''
Created on 07.04.2013

@author: capone
'''

from crashtec.infrastructure.public import definitions

COMMAND_ANALYZE_V = '!analyze -v'
COMMAND_LIST_THREADSTACKS = "~*kb"
COMMAND_QUIT = 'q'


COMMANDS_MAP = {
                definitions.PROBLEMID_CRASH : [COMMAND_ANALYZE_V,
                                               COMMAND_LIST_THREADSTACKS,
                                               COMMAND_QUIT]
                }