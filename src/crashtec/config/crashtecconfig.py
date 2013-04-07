"""
    Contains system wide configuration of crashtec instance
"""

from crashtec.mover.definitions import AGENT_CLASS_TYPE as CRASHMOVER_CLASS
from crashtec.checker.definitions import AGENT_CLASS_TYPE as CHECKER_CLASS

from crashtec.infrastructure.public.jobsequence import JobSequenceBuilder

from crashtec.infrastructure.dbmodel import TASKS_PLATFORM_FIELD
from crashtec.infrastructure.public import definitions as infradefs

CRAHSTEC_MODULES = ['crashtec.infrastructure',
                    'crashtec.mover',
                    'crashtec.checker',
                    'crashtec.symbolsmngr'
                    ]


X86_SEQUENCE = []
X64_SEQUENCE = []

JOB_SEQUENCE = [
                    JobSequenceBuilder.straight_entry(CRASHMOVER_CLASS),
                    JobSequenceBuilder.straight_entry(CHECKER_CLASS),
                    JobSequenceBuilder.branch_entry(TASKS_PLATFORM_FIELD, 
                                        {infradefs.PLATFORM_WIN32 : X86_SEQUENCE,
                                         infradefs.PLATFORM_WIN64 : X64_SEQUENCE}
                                        )
                ]
