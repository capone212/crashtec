'''
Created on 24.02.2013

@author: capone
'''
#TODO: write unit test    
class StraightEntry(object):
    def __init__(self, class_type):
        self.m_class_type = class_type
    
    def value(self, task_record):
        return self.m_class_type 

class BranchEntry(object):
    def __init__(self, field_name, values_dict, default = None):
        self.field_name = field_name
        self.values_dict = values_dict
        self.default = default
    
    def value(self, task_record):
        field_value = task_record[self.field_name]
        if field_value in self.values_dict:
            return self.values_dict[field_value]
        else:
            return self.default

class JobSequenceBuilder(object):
    @staticmethod
    def straight_entry(class_type):
        return StraightEntry(class_type)
    
    @staticmethod
    def branch_entry(field_name, values_dict, default = None):
        return BranchEntry(field_name, values_dict, default)