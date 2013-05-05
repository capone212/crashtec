'''
Created on 27.03.2013

@author: capone
'''
import re
import logging


#TODO: style!!!!
from crashtec.utils.exceptions import CtGeneralError
from crashtec.utils import windebuggers

_logger = logging.getLogger("symbolsmngr")

def _execute_add_command(binaryNetworkPath, symstore_root, platform_id):
    binaryNetworkPath = binaryNetworkPath.decode('ascii', 'ignore')
    symstore_root = symstore_root.decode('ascii', 'ignore')
    # TODO: think about /t and /v switchs
    commandLine = (r"%s add /r /p /l /f '" % windebuggers.SYMSTORE) + binaryNetworkPath + \
        r"\*.*' /s '" + symstore_root + r"' /t crashtec /v 1000";
    return windebuggers.exec_debugging_tool(commandLine, platform_id) 

# TODO: fix it using windebuggers   
def _execute_delete_command(transactionId, symstore_root):
    transactionId = transactionId.decode('ascii', 'ignore')
    commandLine = r"symstore del /i " + transactionId + r" /s " + symstore_root
    commandLine = str(commandLine)
    _logger.debug(commandLine)
    args = shlex.split(commandLine)
    try:
        return subprocess.check_output(args)
    except subprocess.CalledProcessError as err:
        # TODO: raise exception here
        _logger.error("Deleting binary to simbols store. error: %s", err)

def _parseTransactionIdFromAddOutput(commandOutput):
    #Finding ID...  0000000002
    #
    #SYMSTORE: Number of pointers stored = 503
    #SYMSTORE: Number of errors = 0
    #SYMSTORE: Number of pointers ignored = 3
    #
    #done!
    matchTransaction = re.search(b"Finding ID\.\.\.\s+(\d+)\D", commandOutput);
    if not matchTransaction:
        raise CtGeneralError("Can't find out transaction id for added binaries")
    return str(matchTransaction.group(1))

def add_binary_to_symbol_store(binary_network_path, symstore_root, platform_id):
    _logger.info("Adding binary to Symbol Store: %s", binary_network_path)
    commandOutput = _execute_add_command(binary_network_path, 
                                         symstore_root,
                                         platform_id)
    _logger.debug(commandOutput)
    return _parseTransactionIdFromAddOutput(commandOutput)
    
def delete_binaries_from_transaction(transactionId, symstore_root):
    _logger.info("Deleting binaries from Symbol Store: transaction id: %s", 
                 transactionId)
    commandOutput = _execute_delete_command(transactionId)
    if not commandOutput:
        return str()
    _logger.debug(commandOutput)
    return _parseTransactionIdFromAddOutput(commandOutput)
    