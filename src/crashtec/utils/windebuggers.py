'''
Created on 07.04.2013

@author: capone
'''
import os
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

def exec_debugging_tool(command_line, platform_id, env_vars=os.environ.copy()):
    command_line = PathWrapper.unwrap_app_name(command_line,
                                            get_debugger_root_for(platform_id))
    args = shlex.split(command_line)
    try:
        return subprocess.check_output(args, env=env_vars)
    except subprocess.CalledProcessError as err:
        raise CtGeneralError("Error occurred while executing tool: %s " % err)

VAR_EXECUTABLE_IMAGE_PATH = "_NT_EXECUTABLE_IMAGE_PATH"
VAR_SYMBOLS_IMAGE_PATH = "_NT_SYMBOL_PATH"
 
def exec_cdb(commands_list, platform_id, dump_file,
                        binaries_path=str(), symbols_path=str()):
    if not COMMAND_QUIT in commands_list:
        commands_list.append(COMMAND_QUIT)
    # Prepare commands
    SEPARATOR = ";";
    command_line = '%s -lines -z "%s" -c "%s"' % (CDB, dump_file, 
                                        SEPARATOR.join(commands_list))
    # Set image and symbols image path
    cdb_env = os.environ.copy() 
    cdb_env[VAR_EXECUTABLE_IMAGE_PATH] = binaries_path
    cdb_env[VAR_SYMBOLS_IMAGE_PATH] = symbols_path
    
    return exec_debugging_tool(command_line, platform_id, cdb_env)

