"""
    Contains system wide configuration of crashtec instance
"""

import crashtec.crashmover.definitions
import crashtec.checker.definitions


CRAHSTEC_MODULES = ['crashtec.crashmover']


WIN32_JOB_SEQUENCE = [crashtec.crashmover.definitions.EXECUTOR_CLASS_NAME,
                      crashtec.checker.definitions.EXECUTOR_CLASS_NAME
                      ]
