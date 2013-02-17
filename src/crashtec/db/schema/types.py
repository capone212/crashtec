
class DBSchemaTypes (object):
    """DB schema types descriptor"""
    @staticmethod
    def int():
        return "int"
    
    @staticmethod
    def bool():
        return "bool"
    
    @staticmethod
    def float():
        return "float"
    
    @staticmethod
    def datetime():
        return "datetime"
    
    @staticmethod
    def short_string():
        """ 32 length character string"""
        return "short_string"
    
    @staticmethod
    def string():
        """ 256 length character string"""
        return "string"
    
    @staticmethod
    def long_string():
        """ 1024 length character string"""
        return "long_string"
    
    @staticmethod
    def autoincrement():
        return "autoincrement" 


