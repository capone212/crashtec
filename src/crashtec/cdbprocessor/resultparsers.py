'''
Created on 20.04.2013

@author: capone
'''
import re
from crashtec.utils import modules

import callstackparser
from resultspublisher import results_metaclass 

class Parser(object):
    '''Responsible for parsing output of cdb debugger.
    
    Delegates parsing operation to list of specialized 
    parser-objects -- SectionParsers. Each SectionParser responsible for 
    extracting one well defined entity from the debugger output,
    for example crash call stack, loaded modules list, exception code and so on.
    
    All SectionParsers receives the same input (raw debugger output),
    and they expected to return visitable object with parsing operation result.
    '''
    
    def __init__(self, parsers_list):
        self.parsers = parsers_list
        
    # Returns iteratable container of parsed results  
    def parse_output(self, debugger_output):
        return (parser.parse(debugger_output) for parser in self.parsers)

ModulesParserResuls = results_metaclass('ModulesSectionParserResults')  
RawOutputParserResults = results_metaclass('RawOutpuSectionParserResults')
CrashSignatureParserResults = results_metaclass('CrashSignatureParserResults') 

# Parses loaded modules info.
class ModulesSectionParser(object):
    def parse(self, input_string):
        return ModulesParserResuls(modules.parse_modules_info(input_string))

# Simply returns unparsed result    
class RawOutpuSectionParser(object):
    def parse(self, input_string):
        return RawOutputParserResults(input_string)


class CrashSignature(object):
    def __init__(self, problem_class, image_name, 
                        symbol_name, failure_bucket_id):
        self.problem_class = problem_class
        self.image_name = image_name
        self.symbol_name = symbol_name
        self.failure_bucket_id = failure_bucket_id
        
class CrashSignatureParser(object):
    
    def parse(self, raw_cdb_output):
        return CrashSignatureParserResults(
                                    self.do_parse(raw_cdb_output))
    
    def do_parse(self, raw_cdb_output):
        return CrashSignature(
            self.get_value_for_id(raw_cdb_output, 'PRIMARY_PROBLEM_CLASS'),
            self.get_value_for_id(raw_cdb_output, 'IMAGE_NAME'),
            self.get_value_for_id(raw_cdb_output, 'SYMBOL_NAME'),
            self.get_value_for_id(raw_cdb_output, 'FAILURE_BUCKET_ID')
            )
    
    def get_value_for_id(self, raw_cdb_output, key):
        re_key_value = key + r':\s+(\S+)'
        match = re.search(re_key_value, raw_cdb_output)
        if not match:
            print "can't parse value for id %s" % key
            return str()
        return  match.group(1)


def create_parser():
    return Parser([ModulesSectionParser(),
                   RawOutpuSectionParser(),
                   CrashSignatureParser(),
                   callstackparser.ProblemStackParser()
                   ])
    
