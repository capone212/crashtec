import unittest, os
from crashtec.utils import modules
import logging
from crashtec.utils import debug

        

class TestModuleParser(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        cls.logger = logging.getLogger('test')
        debug.init_debug_logger(cls.logger)
    
    def test_get_module_by_imagename(self): 
        TEST_CASES = { 
                "ntdll.dll" : "C:/Windows/SysWOW64/ntdll.dll",
                "Audio.dll" : "C:/Program Files (x86)/AxxonSoft/AxxonSmart/bin/Audio.dll",
                "TAO_Codeset.dll" : "C:/Windows/System32/TAO_Codeset.dll",
            }
        modules_info = modules.Modules(self.logger, os.path.dirname(__file__) + \
                        "/testData/406/AppHost-4408-APP_HOST.Ipint_12-11-07_2011-12-16.dmp")
        for module_name in TEST_CASES.keys():
            self.assertEqual(TEST_CASES[module_name], modules_info.get_module_by_imagename(module_name).image_path)
    
    def test_get_module_mask(self): 
        TEST_CASES = { 
                "ntdll.dll" : "C:/Windows/SysWOW64/.+",
                "Audio.dll" : "C:/Program Files \\(x86\\)/AxxonSoft/AxxonSmart/bin/.+",
                "TAO_Codeset.dll" : "C:/Windows/System32/.+"
            }
        modules_info = modules.Modules(self.logger, os.path.dirname(__file__) + \
                        "/testData/406/AppHost-4408-APP_HOST.Ipint_12-11-07_2011-12-16.dmp")
        for module_name in TEST_CASES.keys():
            self.assertEqual(TEST_CASES[module_name], modules_info.get_module_by_imagename(module_name).get_module_dirrectory_mask())
 

if __name__ == '__main__':
    unittest.main()
