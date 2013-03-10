'''
Created on 18.02.2013

@author: anzor.apshev
'''

class _AggregatedCondition(object):
    def __init__(self, lvalue, tag, rvalue):
        self.m_lvalue = lvalue
        self.m_tag = tag
        self.m_rvalue = rvalue
    
    def to_sql(self):
        (lvalue_sql, lvalue_params) = self.m_lvalue.to_sql()
        (rvalue_sql, rvalue_params) = self.m_rvalue.to_sql()
        sql_string = "(%s) %s (%s)" % (lvalue_sql, self.m_tag, rvalue_sql)
        
        tuple_params = dict(lvalue_params)
        tuple_params.update(rvalue_params)
        return (sql_string, tuple_params)

class _ConditionBase(object):
    # todo: replace with values
    def __init__(self, field, tag, value):
        self.m_field = field
        self.m_tag = tag
        self.m_value = value
    # | operator
    def __or__(self, other):
        return _AggregatedCondition(self, 'or', other)
    # & operator
    def __and__(self, other):
        return _AggregatedCondition(self, 'and', other)
    
    def to_sql(self):
        value_id = "%s%s" % (self.m_field, id(self.m_value))
        sql_string = "%s %s %%(%s)s" % (self.m_field, self.m_tag, value_id)
        sql_params = {value_id : self.m_value}
        return (sql_string, sql_params)
 
 
class FieldFilterFactory(object):
    def __init__(self, field):
        self.m_field = field
    
    def greater_than(self, value):
        return _ConditionBase(self.m_field, '>', value)
    
    def equal_to(self, value):
        return _ConditionBase(self.m_field, '=', value)
    
    def not_equal_to(self, value):
        return _ConditionBase(self.m_field, '!=', value)
    
    def less_than(self, value):
        return _ConditionBase(self.m_field, '<', value)
    
    def less_or_equal(self, value):
        return _ConditionBase(self.m_field, '<=', value)
    
    def greater_or_equal(self, value):
        return _ConditionBase(self.m_field, '>=', value)
    
    def __gt__(self, value):
        return self.greater_than(value)
    
    def __eq__(self, value):
        return self.equal_to(value)
    
    def __lt__(self, value):
        return self.less_than(value)
    
    def __le__(self, value):
        return self.less_or_equal(value)
    
    def __ge__(self, value):
        return self.greater_or_equal(value)
    
    def __ne__(self, value):
        return self.not_equal_to(value)


class Descent(object):
    def __init__(self, column_name):
        self.column_name = column_name
    
    def to_sql(self):
        return '%s DESC' % self.column_name
    
class Ascent(object):
    def __init__(self, column_name):
        self.column_name = column_name
    
    def to_sql(self):
        return '%s ASC' % self.column_name

#f = FieldFilterFactory
#h = (f('agent_instance_name') != 'hello')  | (f('agent_instance_name') == 'hell') 
#
#print h.to_sql()