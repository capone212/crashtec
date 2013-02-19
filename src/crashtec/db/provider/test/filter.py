'''
Created on 19.02.2013

@author: anzor.apshev
'''
import crashtec.db.provider.filter as pfilter
import unittest

f = pfilter.FieldFilterFactory('field')

class TestFileldFilterFactory(unittest.TestCase):
    
    # This test cases actually ugly, because they test implementation details
    # but, unfortunately we could not validate sql substrings,
    # so hopefully following is better than nothing.
    def test_greater_than(self):
        cond = f.greater_than(0)
        self.assertEqual(cond.m_tag, '>')
        
    def test_equal_to(self):
        cond = f.equal_to(0)
        self.assertEqual(cond.m_tag, '=')
        
    def test_not_equal_to(self):
        cond = f.not_equal_to(0)
        self.assertEqual(cond.m_tag, '!=')
    
    def test_less_than(self):
        cond = f.less_than(0)
        self.assertEqual(cond.m_tag, '<')
    
    def test_less_or_equal(self):
        cond = f.less_or_equal(0)
        self.assertEqual(cond.m_tag, '<=')

    def test_greater_or_equal(self):
        cond = f.greater_or_equal(0)
        self.assertEqual(cond.m_tag, '>=')
        
    # These checks that operator overloads call the same behavior as operators
    def test_gt(self):
        cond1 = f.greater_than(0)
        cond2 = f > 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())
        
    def test_eq(self):
        cond1 = f.equal_to(0)
        cond2 = f == 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())
        
    def test_ne(self):
        cond1 = f.not_equal_to(0)
        cond2 = f != 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())

    def test_lt(self):
        cond1 = f.less_than(0)
        cond2 = f < 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())

    def test_le(self):
        cond1 = f.less_or_equal(0)
        cond2 = f <= 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())

    def test_ge(self):
        cond1 = f.greater_or_equal(0)
        cond2 = f >= 0 
        self.assertEqual(cond1.to_sql(), cond2.to_sql())


if __name__ == '__main__':
    unittest.main()
