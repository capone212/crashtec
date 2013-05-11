'''
Created on 12.03.2013

@author: anzor.apshev
'''
import re

from crashtec.utils.exceptions import CtGeneralError
from crashtec.utils import windebuggers
from crashtec.config import checkerconfig
from crashtec.infrastructure.public import definitions as infradefs

import definitions

def execute_dump_checker(dump_file_name):
    commandLine = "%s '%s'" % (checkerconfig.DUMP_CHECKER_TOOL, dump_file_name)
    # Execute x64 version of dump_check to avoid interoperability risks
    return windebuggers.exec_debugging_tool(commandLine, 
                                     infradefs.PLATFORM_WIN64)

_PLATFORMS_MAP = {
                  'PROCESSOR_ARCHITECTURE_AMD64' : infradefs.PLATFORM_WIN64,
                  'PROCESSOR_ARCHITECTURE_INTEL' : infradefs.PLATFORM_WIN32,
                  }

def parse_checker_output(checker_output):
    if (not checker_output):
        raise CtGeneralError('empty input passed to parse_checker_output')
    SUCCESS_STRING = 'Finished dump check'
    checker_output = checker_output.rstrip('\r\n')
    if (not checker_output.endswith(SUCCESS_STRING)):
        raise CtGeneralError("Can't parse dump checker response."\
                             " Probably invalid dump passed.")
    #   ProcessorArchitecture   0000 (PROCESSOR_ARCHITECTURE_INTEL)
    # todo
    re_cpu_architecture = r"ProcessorArchitecture\s+\d+\s+\(([^)]+)\)"
    matchObj = re.search(re_cpu_architecture, checker_output)
    if (not matchObj):
        raise CtGeneralError("Can't parse dump checker response."\
                             " Probably unknown output format.")
    cpu_architecture = matchObj.group(1)
    if not (cpu_architecture in _PLATFORMS_MAP):
        raise CtGeneralError("Unknown CPU architecture %s." % \
                              cpu_architecture)
    # TODO: handle linux platforms in future
    return {definitions.PLATFORM_PARAM : _PLATFORMS_MAP[cpu_architecture]}


    
    