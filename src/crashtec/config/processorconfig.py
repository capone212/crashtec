'''
Created on 07.04.2013

@author: capone
'''

from crashtec.infrastructure.public import definitions
from crashtec.utils import windebuggers as wd

COMMANDS_MAP = {
                definitions.PROBLEMID_CRASH : [wd.COMMAND_ANALYZE_V,
                                               wd.COMMAND_LIST_THREADSTACKS,
                                               wd.COMMAND_QUIT]
                }