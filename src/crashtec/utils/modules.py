'''
Created on 16.03.2013

@author: capone
'''
import shlex
import subprocess
import re
import os

from crashtec.utils.exceptions import CtGeneralError

def escape_re_characters(input):
    # \\ should be the first character to screen
    RE_ESCAPE_CHARACTERS = "\\.^$*+?{}[]|()"
    for ch in RE_ESCAPE_CHARACTERS:
        input = input.replace(ch, "\\"+ch)
    return input
    
class ModuleInfo(object):
    def __init__(self, parser_match):
        self.module_name = parser_match.group("module_name")
        self.image_path = parser_match.group("image_name").replace("\\", "/")
        self.version = parser_match.group("file_version")
        self.image_name = os.path.basename(self.image_path)
    
    def get_module_dirrectory_mask(self):
        return escape_re_characters(os.path.dirname(self.image_path)) + "/.+"

class Modules(object):
    """A class for representing modules from memory dump (lm command of Windbg)"""
    def __init__(self, logger, dump_file_name):
        try:
            self.logger = logger
            cdb_output = _list_dump_modules(dump_file_name)
            self.modules_list = _parse_modules_info(cdb_output)
        except subprocess.CalledProcessError as err:
            self.logger.error("CalledProcessError exception while listing modules: code = %s message %s",
                  err.returncode, err.output)
            raise CtGeneralError("Can't list dump modules: CalledProcessError")
        except RuntimeError as err:
            self.logger.error("RuntimeError occurred while listing modules: %s", str(err))
            raise CtGeneralError("Can't list dump modules: RuntimeError")
    
    # Module name with extention, for example 'rcpp.dll' 
    def get_module_by_imagename(self, name):
        for module in self.modules_list:
            if (name.lower() == module.image_name.lower()):
                return module
        return None
    
    # Module name in debugger, for example 'rcpp'
    def get_module_by_modulename(self, moduleName):
        for module in self.modules_list:
            if module.module_name == moduleName:
                return module

def _list_dump_modules(dumpFile):
    commandLine = "cdb -z \"" + dumpFile + \
    "\" -c \"!for_each_module .echo ModuleName = '@#ModuleName' FileVersion = '@#FileVersion' ImageName = '@#ImageName';q\"";
    args = shlex.split(commandLine)
    return subprocess.check_output(args)

def _parse_modules_info(inputString):
#ModuleName = 'AxxonNext' FileVersion = '3.0.0.465' ImageName = 'C:\Program Files\AxxonSoft\AxxonSmart\bin\AxxonNext.exe'
    reModulesExpr = "(?<=\n)ModuleName = '(?P<module_name>[^']+)' FileVersion = '(?P<file_version>[^']+)' ImageName = '(?P<image_name>[^']+)'"
    modulesIterator = re.finditer(reModulesExpr, inputString)
    result = []
    for module in modulesIterator:
        result.append(ModuleInfo(module))
    return result

