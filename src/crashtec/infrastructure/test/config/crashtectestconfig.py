'''
Created on 31.03.2013

@author: capone
'''
"""
    Contains test configuration of crashtec instance
"""

from crashtec.infrastructure.public.jobsequence import JobSequenceBuilder

from crashtec.infrastructure.dbmodel import TASKS_PLATFORM_FIELD
from crashtec.infrastructure.public import definitions as infradefs

CRASHMOVER_CLASS = 'mover'
CHECKER_CLASS = 'checker'
PROCESSOR_X86_CLASS = 'processor_x86'
PROCESSOR_X64_CLASS = 'processor_x64'  


X86_SEQUENCE = [JobSequenceBuilder.straight_entry(PROCESSOR_X86_CLASS)]
X64_SEQUENCE = [JobSequenceBuilder.straight_entry(PROCESSOR_X64_CLASS)]

TEST_JOB_SEQUENCE = [
                    JobSequenceBuilder.straight_entry(CRASHMOVER_CLASS),
                    JobSequenceBuilder.straight_entry(CHECKER_CLASS),
                    JobSequenceBuilder.branch_entry(TASKS_PLATFORM_FIELD, 
                                        {infradefs.PLATFORM_WIN32 : X86_SEQUENCE,
                                         infradefs.PLATFORM_WIN64 : X64_SEQUENCE}
                                        )
                     ]
