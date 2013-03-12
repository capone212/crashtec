"""
    Contains system wide configuration of crashtec instance
"""

from crashtec.crashmover.definitions import EXECUTOR_CLASS_NAME as CRASHMOVER_CLASS
from crashtec.checker.definitions import EXECUTOR_CLASS_NAME as CHECKER_CLASS
from crashtec.infrastructure.public.jobsequence import JobSequenceBuilder

CRAHSTEC_MODULES = ['crashtec.crashmover']


JOB_SEQUENCE = [
                JobSequenceBuilder.straight_entry(CRASHMOVER_CLASS),
                JobSequenceBuilder.straight_entry(CHECKER_CLASS)
                ]
