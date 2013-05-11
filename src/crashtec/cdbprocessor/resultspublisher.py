'''
Created on 04.05.2013

@author: capone
'''

from crashtec.db.provider import routines as dbroutines
from crashtec.db.schema.fields import PRIMARY_KEY_FIELD

import dbmodel

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
        raise RuntimeError("shouldn't be called!")

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
    
    # It is important that task here took by reference, so we can update
    # task record as well.
    def __init__(self, task):
            self.task = task
    
    def visit_ModulesSectionParserResults(self, modules_list):
        pass
    
    def visit_RawOutpuSectionParserResults(self, raw_debugger_output):
        raw_debugger_output = raw_debugger_output.decode('ascii', 'ignore')
        d = dbmodel
        new_record = dbroutines.Record()
        new_record[d.RAWRESULTS_TASK_ID] = self.task[PRIMARY_KEY_FIELD]
        new_record[d.RAWRESULTS_DBG_OUTPUT] = raw_debugger_output
        dbroutines.create_new_record(d.RAWRESULTS_TABLE, new_record)
    
    def visit_CrashSignatureParserResults(self, crash_signature):
        d = dbmodel
        self.task[d.TASKS_PROBLEM_CLASS] = crash_signature.problem_class
        self.task[d.TASKS_SYMBOL_NAME] = crash_signature.symbol_name
        self.task[d.TASKS_FAIL_IMAGE] = crash_signature.image_name
        self.task[d.TASKS_FAILURE_BUCKET_ID] = crash_signature.failure_bucket_id
        
    
    def visit_ProblemStackParserResuls(self, crash_call_stack):
        pass