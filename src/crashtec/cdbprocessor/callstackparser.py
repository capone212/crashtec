'''
Created on 27.04.2013

Contains primitives for parsing threads call stacks from cdb.exe output

@author: capone
'''
import re
import logging

from resultspublisher import results_metaclass


_logger = logging.getLogger("cdb_processor")


class StackEntry(object):
    
    '''Represents a single line (in fact function call) in thread call-stack.'''
    
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

# Visitable wrapper for results of ProblemStackParser 
ProblemStackParserResuls = results_metaclass('ProblemStackParserResuls')  

# TODO: separate actual stack parsing with  SectionParser mechanics. 
# It will allow return results_metaclass to parsers module and reuse stack 
# parsing in another section parsers


class ProblemStackParser(object):
    
    '''Extracts and parses crash stack from debugger output.'''
    
    def parse(self, raw_cdb_output):
        return ProblemStackParserResuls(self.do_parse(raw_cdb_output))
    
    def do_parse(self, raw_cdb_output):
        '''
        Receives cdb debugger output and returns list of StackEntry objects.
        '''
        stack_lines = self.extrack_stack_lines(raw_cdb_output)
        refined_lines = self.strip_additional_info(stack_lines)
        return [StackEntry(line) for line in refined_lines]
     
    def extrack_stack_lines(self, raw_cdb_output):
        '''Returns problem thread call stack lines as list of strings.'''
        
        # matches 
        #    STACK_TEXT:\n
        #    something\n
        #    something\n
        #    \n
        reStartExpression = "STACK_TEXT:\s*\n"
        match = re.search(reStartExpression, raw_cdb_output)
        if (not match):
            return []
        inputString = raw_cdb_output[match.end():]
        match = re.search("\n\n", inputString)
        if (not match):
            return []
        inputString = inputString[:match.start()]
        return  re.split("\n", inputString, maxsplit=0, flags=0)
    
    def strip_additional_info(self, stack_lines):
        '''
        Returns stack line without addresses, param and source files info
        
        For example:  
           0454f544 71e58e89 e06d7363 00000001 00000003 KERNELBASE!RaiseException+0x58
        Will be converted to 
           KERNELBASE!RaiseException+0x58
        '''
        # FIXME: use task info here to chose appropriate function
        x86_result = self.strip_additional_info_x86(stack_lines)
        if x86_result:
            return x86_result
        return self.strip_additional_info_x64(stack_lines)
        
    
    def strip_additional_info_x86(self, stack_lines):
        #0454f544 71e58e89 e06d7363 00000001 00000003 KERNELBASE!RaiseException+0x58
        re_hex = "[0-9a-fA-F]+" 
        re_stack_line = "(" + re_hex + "\s+){2,5}(?P<signature>.+)"
        return self.strip_additional_info_impl(stack_lines, re_stack_line)
    
    def strip_additional_info_x64(self, stack_lines):
        #'00000000`0619efa0 00000000`00000000 : 0000006e`6f697400 000007fe`f1beaca0 00000000`00000000 00000000`00000000 : Ipint_SonyIpela+0x16acb0'
        re_64_address = "[0-9a-fA-F`]+"
        re_separator = r"(\s|:)+"
        re_stack_line = "(" + re_64_address + re_separator +"){4,6}(?P<signature>.+)"
        return self.strip_additional_info_impl(stack_lines, re_stack_line)
    
    def strip_additional_info_impl(self, stack_lines, re_stack_line):
        signatures = []
        for line in stack_lines:
            match = re.search(re_stack_line, line)
            if (not match):
                _logger.warning("Can't parse signature string: %s", line)
                continue
            signatures.append(match.group('signature'))
        # TODO: replace with generator expression
        return [self.strip_source_info(signature) for signature in signatures]
    
    def strip_source_info(self, signature):
        ''' Stack line in signature + source info,
             so we want to strip source info'''
        signature = signature.strip()
        reSourceInfo = r" \[[^\]]+\]$"
        match = re.search(reSourceInfo, signature)
        if not match:
            return signature
        return signature[:match.start()]
