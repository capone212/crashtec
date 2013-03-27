'''
Created on 27.03.2013
    HB! :)
@author: capone
'''
import urlparse
import logging

from crashtec.db.provider import routines
from crashtec.db.provider import filter
from crashtec.utils.exceptions import CtGeneralError

import dbmodel
import symstoredetails
import definitions

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

class SymbolsStore(object):
    # Add's binaries to symbol store.
    # param urls_list - a list of url to zip files with binary data. 
    def add_binaries_from_urls(self, urls_list):
        for url in urls_list:
            # Lookup current url in binary database
            result = _select_binary_by_url(url)
            if (result):
                _logger.info("detected binary dir: %s", result.local_dir)
                self._add_existing_binary_path(result)
                continue
#            #doSYMBOLS_TRANSACTION_ID are not registred in db
#            binaryDirrectory = downloadAndUnzipUrl(url)
#            if (not binaryDirrectory):
#                continue;
#            binaryDirrectory = definitions.convertToNetworkPath(binaryDirrectory)
#            # update itv symbols store
#            transactionId = symbolsStoreProvider.add_binary_to_symbol_store(binaryDirrectory)
#            if not transactionId:
#                return
#            #update database
#            dbUtils.addBinary(url, binaryDirrectory, transactionId, databaseCursor)
    
    def _add_existing_binary_path(self, binary):
        if (binary.symstore_transaction_id != definitions.EMPTY_TRANSACTION):
            # Binary is already in symstore
            return
        _logger.info("Binary is not added to symbol store. Adding...")
        transactionId = symstoredetails.add_binary_to_symbol_store(binary.local_dir)
       # todo: CONTINUE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111111111
        dbUtils.updateTransactionIdForBinary(binary.dirPath, transactionId, databaseCursor)
        _logger.info("Binary successfully added to symbol store")


class BinaryRecord:
    """A class for representing a binary table record"""
    url = str()
    local_dir = str()
    symstore_transaction_id = str()

# Returns BinaryRecord instance  
def _select_binary_by_url(binary_url):
    parsed_url = urlparse.urlparse(binary_url)
    if (not parsed_url):
        raise CtGeneralError("Could not parse url for request binary location on db: %s" % binary_url)
    d = dbmodel
    f = filter.FieldFilterFactory
    cursor = routines.select_from(d.SYMBOLS_TABLE, filter = f(d.SYMBOLS_URL) == parsed_url.path)
    result = cursor.fetchone()
    if not result:
        return None
    record = BinaryRecord()
    # move to separate function 
    record.url = result[d.SYMBOLS_URL]
    record.local_dir = result[d.SYMBOLS_LOCAL_DIR]
    record.symstore_transaction_id = result[d.SYMBOLS_TRANSACTION_ID]
    return record
