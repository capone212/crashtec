'''
Created on 27.03.2013

@author: capone
'''
import subprocess
import shlex
import re
import logging

#TODO: style!!!!

from crashtec.utils.exceptions import CtGeneralError
from crashtec.config import symbolsmngrconfig
_logger = logging.getLogger("symbolsmngr.symbolsmngr")

def _execute_add_command(binaryNetworkPath):
    binaryNetworkPath = binaryNetworkPath.decode('ascii', 'ignore')
    # TODO: think about /t and /v switchs
    commandLine = r"symstore add /r /p /f '" + binaryNetworkPath + r"*.*' /s " + symbolsmngrconfig.SYMBOLS_STORE_LOCAL_DIR + \
        r" /t crashtec /v 1000";
    commandLine = str(commandLine)
    _logger.debug(commandLine)
    args = shlex.split(commandLine)
    try:
        return subprocess.check_output(args)
    except subprocess.CalledProcessError as err:
        raise CtGeneralError("Add binary to symbols store. error: %" % err)
        
def _execute_delete_command(transactionId):
    transactionId = transactionId.decode('ascii', 'ignore')
    commandLine = r"symstore del /i " + transactionId + r" /s " + symbolsmngrconfig.SYMBOLS_STORE_LOCAL_DIR;
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

def add_binary_to_symbol_store(binary_network_path):
    _logger.info("Adding binary to Symbol Store: %s", binary_network_path)
    commandOutput = _execute_add_command(binary_network_path)
    _logger.debug(commandOutput)
    return _parseTransactionIdFromAddOutput(commandOutput)
    
def delete_binaries_from_transaction(transactionId):
    _logger.info("Deleting binaries from Symbol Store: transaction id: %s", transactionId)
    commandOutput = _execute_delete_command(transactionId)
    if not commandOutput:
        return str()
    _logger.debug(commandOutput)
    return _parseTransactionIdFromAddOutput(commandOutput)
    