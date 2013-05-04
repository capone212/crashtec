'''
Created on 04.05.2013

@author: capone
'''

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

# Visitor responsible for saving crash dump processing results. 
class ResultsPublisher(object):
    
    def visit_ModulesSectionParserResults(self, modules_list):
        pass
    
    def visit_RawOutpuSectionParserResults(self, raw_debugger_output):
        pass
    
    def visit_CrashSignatureParserResults(self, crash_signature):
        pass
    
    def visit_ProblemStackParserResuls(self, crash_call_stack):
        pass