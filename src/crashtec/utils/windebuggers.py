'''
Created on 07.04.2013

@author: capone
'''
import subprocess
import shlex

from crashtec.utils.exceptions import CtGeneralError
from crashtec.config import windowsconfig
from crashtec.infrastructure.public import definitions

# CDB commands list
COMMAND_ANALYZE_V = '!analyze -v'
COMMAND_LIST_THREADSTACKS = "~*kb"
COMMAND_QUIT = 'q'
COMMAND_LIST_MODULES = "!for_each_module .echo ModuleName = '@#ModuleName'" \
        " FileVersion = '@#FileVersion' ImageName = '@#ImageName'"


class PathWrapper(object):
    ROOT_DIR_PLACEHOLDER = "{root_dir}"
    @classmethod
    def wrap_app_name(cls, name):
        return '"%s/%s"' % (cls.ROOT_DIR_PLACEHOLDER, name)
    
    @classmethod
    def unwrap_app_name(cls, name, tool_dir):
        return name.replace(cls.ROOT_DIR_PLACEHOLDER, tool_dir)


CDB = PathWrapper.wrap_app_name('cdb.exe')
SYMSTORE = PathWrapper.wrap_app_name('symstore.exe')
DUMP_CHECKER = PathWrapper.wrap_app_name('dumpchk.exe')

def get_debugger_root_for(platform_id):
    d = definitions;
    wc = windowsconfig
    PLATFORMS_MAP = {
                        d.PLATFORM_WIN32 : wc.X86_DEBUGGERS_ROOT,
                        d.PLATFORM_WIN64 : wc.X64_DEBUGGERS_ROOT                     
                     }
    if not platform_id in PLATFORMS_MAP:
        raise CtGeneralError("Unknown debugger platform: %s" % platform_id)
    return PLATFORMS_MAP[platform_id]

def exec_debugging_tool(command_line, platform_id):
    command_line = PathWrapper.unwrap_app_name(command_line,
                                            get_debugger_root_for(platform_id))
    args = shlex.split(command_line)
    try:
        return subprocess.check_output(args)
    except subprocess.CalledProcessError as err:
        raise CtGeneralError("Error occurred while executing tool: " % err)

def exec_cdb(commands_list, platform_id, dump_file):
    if not COMMAND_QUIT in commands_list:
        commands_list.append(COMMAND_QUIT)
    SEPARATOR = ";";
    command_line = '%s -lines -z "%s" -c "%s"' % (CDB, dump_file, 
                                        SEPARATOR.join(commands_list))
    return exec_debugging_tool(command_line, platform_id)

#exec_cdb([COMMAND_ANALYZE_V, COMMAND_LIST_THREADSTACKS], 
#"win32", "d\\dumps\exec.dmp")

