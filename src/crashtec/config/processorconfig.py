'''
Created on 07.04.2013

@author: capone
'''

from crashtec.infrastructure.public import definitions
from crashtec.utils import windebuggers as wd

# FIXME: support hung problem_id

COMMANDS_MAP = {
                definitions.PROBLEMID_CRASH : [wd.COMMAND_ANALYZE_V,
                                               wd.COMMAND_LIST_THREADSTACKS,
                                               wd.COMMAND_QUIT]
                }

# FIXME: think about custom symbols path. How to support symbols from third?
MS_SYMBOLS_CACHE = 'C:\\symbols'
STANDARD_SYMBOLS_PATH = 'srv*%s*http://msdl.microsoft.com/download/symbols' %\
                MS_SYMBOLS_CACHE