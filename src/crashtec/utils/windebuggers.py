'''
Created on 07.04.2013

@author: capone
'''
import subprocess
import shlex

from crashtec.utils.exceptions import CtGeneralError

def exec_debugging_tool(command_line, platform_id):
    # TODO: handle platfor_id
    args = shlex.split(command_line)
    try:
        return subprocess.check_output(args)
    except subprocess.CalledProcessError as err:
        raise CtGeneralError("Error occured while executing tool: " % err)

