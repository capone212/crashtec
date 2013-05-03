'''
Created on 27.04.2013

@author: capone
'''
import re
import logging

# TODO: dirty implementation from early days 
_logger = logging.getLogger("cdb_processor")

# FIXME: an issue with D:/work/test/tasksRoot/tasksRoot\306\results.txt, stack lnes remains unparsed
# FIXME:  handle "Following stacks may be ..." case. Stop when encounter this line 


# Represents a single line (in fact function call) in thread call-stack.
class StackEntry(object):
    def __init__(self, line):
        self.line = line
    
    def get_line(self):
        return self.line
    
    def get_module_name(self):
        re_module_name = r"([^!@]+)[!@].+"
        match = re.match(re_module_name, self.line)
        if (not match):
            return None
        return match.group(1) 

class SignatureBuilder(object):
    # \param stackLines raw stack line
    # \param modules the ModuleUtils.Module object
    # \return tuple of (signature, truncated, product)
    def build(self, stack_entries):
        result = str()
        for stack_entry in stack_entries: 
            if result:
                result += " | "
            result += stack_entry.get_line()
            module_name = stack_entry.get_module_name()
            if not module_name:
                _logger.debug("Can't extract module name from signature: %s", 
                              stack_entry.get_line())
            #TODO:
            product = modules.getProductByModuleName(module_name)
            if (product):
                (signature, truncated) = _truncateSignature(signature)
                return (signature, truncated, product)
        (result, truncated) =  _truncateSignature(result)
        return (result, truncated, None)
    
    def _truncateSignature(signature):
        MAX_LEN = 255
        if len(signature) > MAX_LEN:
                signature = "%s..." % signature[:MAX_LEN - 3]
                gLogger.debug('SignatureTool: signature truncated due to length')
                return (signature, True)
        return (signature, False)

# Extracts and parses crash stack from debugger output.
class ProblemStackParser(object):
    # Receives cdb debugger output and returns list of StackEntry objects.
    def parse(self, raw_cdb_output):
        stack_lines = self.extrack_stack_lines(raw_cdb_output)
        refined_lines = self.strip_additional_info(stack_lines)
        # TODO: replace with generator expression
        return [StackEntry(line) for line in refined_lines]
    
    # Returns problem thread call stack lines as list of strings 
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
        # TODO: replace with generator expression
        return [self.strip_source_info(signature) for signature in signatures]
    
    # Stack line in signature + source info, so we want to strip source info
    def strip_source_info(self, signature):
        signature = signature.strip()
        reSourceInfo = r" \[[^\]]+\]$"
        match = re.search(reSourceInfo, signature)
        if not match:
            return signature
        return signature[:match.start()] 
    

    