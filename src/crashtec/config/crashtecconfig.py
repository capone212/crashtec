"""
    Contains system wide configuration of crashtec instance
"""

from crashtec.mover.definitions import AGENT_CLASS_TYPE as CRASHMOVER_CLASS
from crashtec.checker.definitions import AGENT_CLASS_TYPE as CHECKER_CLASS

from crashtec.cdbprocessor.definitions import CDB_PROCESSOR_X86_CLASS_TYPE
from crashtec.symbolsmngr.definitions import SYMBOLS_MANAGER_X86_CLASS_TYPE

from crashtec.cdbprocessor.definitions import CDB_PROCESSOR_X64_CLASS_TYPE
from crashtec.symbolsmngr.definitions import SYMBOLS_MANAGER_X64_CLASS_TYPE

from crashtec.infrastructure.public.jobsequence import JobSequenceBuilder as jsb

from crashtec.infrastructure.dbmodel import TASKS_PLATFORM_FIELD
from crashtec.infrastructure.public import definitions as infradefs

CRAHSTEC_MODULES = ['crashtec.infrastructure',
                    'crashtec.mover',
                    'crashtec.checker',
                    'crashtec.symbolsmngr',
                    'crashtec.cdbprocessor'
                    ]

X86_SEQUENCE = [
                jsb.straight_entry(SYMBOLS_MANAGER_X86_CLASS_TYPE),
                jsb.straight_entry(CDB_PROCESSOR_X86_CLASS_TYPE)
                ]

X64_SEQUENCE = [
                jsb.straight_entry(SYMBOLS_MANAGER_X64_CLASS_TYPE),
                jsb.straight_entry(CDB_PROCESSOR_X64_CLASS_TYPE)
                ]

JOB_SEQUENCE = [
                    jsb.straight_entry(CRASHMOVER_CLASS),
                    jsb.straight_entry(CHECKER_CLASS),
                    jsb.branch_entry(TASKS_PLATFORM_FIELD, 
                                    {infradefs.PLATFORM_WIN32 : X86_SEQUENCE,
                                     infradefs.PLATFORM_WIN64 : X64_SEQUENCE})
                ]

""" Defines agents instances keep-alive timeout in seconds"""
AGENTS_KEEPALIVE_TIMEOUT = 10; 