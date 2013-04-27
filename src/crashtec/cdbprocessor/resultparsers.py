'''
Created on 20.04.2013

@author: capone
'''
from crashtec.utils import modules 

class Acceptor(object):
    def __init__(self, class_name):
        self.class_name = class_name
    
    def __call__(self, instance, visitor):
        visit_method = getattr(visitor, 'visit_%s' % self.class_name)
        visit_method(instance.parser_results)

class BaseResult(object):
    def __init__(self, parser_results):
        self.parser_results = parser_results
    
    def accept(self, visitor):
        return self.delegated_accept(self, visitor)
    
    # should be implemented in subclasses
    def delegated_accept(self, instance, visitor):
        raise RuntimeError("should't be called!")

def results_metaclass(class_name):
    return type(class_name,
                (BaseResult,),
                {'delegated_accept' : Acceptor(class_name)})

ModulesParserResuls = results_metaclass('ModulesParserResults')  
RawOutputParserResults = results_metaclass('RawOutputParserResults')   

class ModulesParser(object):
    def parse(self, input_string):
        return ModulesParserResuls(modules.parse_modules_info(input_string))

# Simply returns unparsed result    
class RawOutputParser(object):
    def parse(self, input_string):
        return RawOutputParserResults(input_string)


class Parser(object):
    def __init__(self, parsers_list):
        self.parsers = parsers_list
        
    # Returns iteratable container of parsed results  
    def parse_output(self, debugger_output):
        # FIXME: Use generator expression here for saving memory 
        return (parser.parse(debugger_output) for parser in self.parsers)

def create_parser():
    return Parser([ModulesParser(),
                   RawOutputParser()
                   ])
    
