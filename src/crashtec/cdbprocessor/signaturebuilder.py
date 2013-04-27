'''
Created on 27.04.2013

@author: capone
'''
import re
import logging

# TODO: dirty implementation from early days 
_logger = logging.getLogger("cdb_processor")

class StackEntry(object):
    def __init__(self, line):
        self.line = line
    
    def get_line(self):
        return self.line
    
    def get_module_name(self):
        reModuleName = r"([^!@]+)[!@].+"
        match = re.match(reModuleName, self.line)
        if (not match):
            return None
        return match.group(1) 
    

class ProblemStackParser(object):
    # Returns problem thread stack lines as list of string 
    def extrack_stack_lines(self, raw_cdb_output):
        # matches 
        #    STACK_TEXT:\n
        #    something\n
        #    something\n
        #    \n
        #reStartExpression = b"STACK_TEXT:\n(?!\n\n)\n\n"
        reStartExpression = "STACK_TEXT:\s*\n"
        match = re.search(reStartExpression, raw_cdb_output)
        if (not match):
            return None
        inputString = raw_cdb_output[match.end():]
        match = re.search("\n\n", inputString)
        if (not match):
            return None
        inputString = inputString[:match.start()]
        return  re.split("\n", inputString, maxsplit=0, flags=0)
    
    # Returns stack line without addresses, param and source files info
    # For example:  
    #    0454f544 71e58e89 e06d7363 00000001 00000003 KERNELBASE!RaiseException+0x58
    # Will be converted to 
    #    KERNELBASE!RaiseException+0x58
    def strip_additional_info(self, stack_lines):
        reHex = "[0-9a-fA-F]+" 
        reStackLine = "(" + reHex + "\s+){5}(?P<signature>.+)"
        #0454f544 71e58e89 e06d7363 00000001 00000003 KERNELBASE!RaiseException+0x58
        signatures = []
        for line in stack_lines:
            match = re.search(reStackLine, line)
            if (not match):
                _logger.warning("Can't parse signature string: %s", line)
                continue
            signatures.append(match.group('signature'))
        return [self.strip_source_info(signature) for signature in signatures]
    
    #TODO: write unit test on it 
    # Stack line in signature + source info, so we want to strip source info
    def strip_source_info(self, signature):
        signature = signature.strip()
        reSourceInfo = r" \[[^\]]+\]$"
        match = re.search(reSourceInfo, signature)
        if not match:
            return signature
        return signature[:match.start()] 