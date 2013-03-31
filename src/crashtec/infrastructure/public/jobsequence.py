'''
Created on 24.02.2013

@author: capone
'''

class StraightEntry(object):
    def __init__(self, class_type):
        self.class_type = class_type
    
    def accept(self, visitor):
        return visitor.visit_straight_entry(self)
    
class BranchEntry(object):
    def __init__(self, field_name, values_dict, default = None):
        self.field_name = field_name
        self.values_dict = values_dict
        self.default = default
    
    def accept(self, visitor):
        return visitor.visit_branch_entry(self)
    

class JobSequenceBuilder(object):
    @staticmethod
    def straight_entry(class_type):
        return StraightEntry(class_type)
    
    @staticmethod
    def branch_entry(field_name, values_dict, default = None):
        return BranchEntry(field_name, values_dict, default)

class GetJobEntryValueVisitor(object):
    def __init__(self, task_record):
        self.task_record = task_record
        self.obtained_value = None
    
    # Visitor interface methods
    def visit_straight_entry(self, straight_entry):
        return straight_entry.class_type
    
    def visit_branch_entry(self, branch_entry):
        field_value = self.task_record[branch_entry.field_name]
        if field_value in branch_entry.values_dict:
            return branch_entry.values_dict[field_value]
        else:
            return branch_entry.default
    