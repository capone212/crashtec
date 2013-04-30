'''
Created on 20.04.2013

@author: capone
'''
from crashtec.utils import modules 

# Responsible for parsing output of cdb debugger.
# Deligates parsing operation to list of specialized parser-objects -- SectionParsers.
# Each SectionParser responsible for extracting one well defined entity from the 
# debugger output, for example crash call stack, loaded modules list, exception code and so on.
# All SectionParsers receives the same input (raw debugger output),
# and they expected to return visitable object with parsing operation result.
class Parser(object):
    def __init__(self, parsers_list):
        self.parsers = parsers_list
        
    # Returns iteratable container of parsed results  
    def parse_output(self, debugger_output):
        # FIXME: Use generator expression here for saving memory 
        return (parser.parse(debugger_output) for parser in self.parsers)

# Utility class which used to make hack with meta-classes. See results_metaclass()  
class Acceptor(object):
    def __init__(self, class_name):
        self.class_name = class_name
    
    def __call__(self, instance, visitor):
        visit_method = getattr(visitor, 'visit_%s' % self.class_name)
        visit_method(instance.parser_results)

# Utility class which used to make hack with meta-classes. See results_metaclass()
class BaseResult(object):
    def __init__(self, parser_results):
        self.parser_results = parser_results
    
    def accept(self, visitor):
        return self.delegated_accept(self, visitor)
    
    # should be implemented in subclasses
    def delegated_accept(self, instance, visitor):
        raise RuntimeError("should't be called!")

# Metaclass which generates wrapper classes for primitive parser results. 
# Wrapper implements all necesserary methods for supporting visitors.
# Main intention of this trick is prevent code duplication.
# For example: If 
def results_metaclass(class_name):
    return type(class_name,
                (BaseResult,),
                {'delegated_accept' : Acceptor(class_name)})

ModulesParserResuls = results_metaclass('ModulesSectionParserResults')  
RawOutputParserResults = results_metaclass('RawOutpuSectionParserResults')   

# Parses loaded modules info.
class ModulesSectionParser(object):
    def parse(self, input_string):
        return ModulesParserResuls(modules.parse_modules_info(input_string))

# Simply returns unparsed result    
class RawOutpuSectionParser(object):
    def parse(self, input_string):
        return RawOutputParserResults(input_string)


def create_parser():
    return Parser([ModulesSectionParser(),
                   RawOutpuSectionParser()
                   ])
    
