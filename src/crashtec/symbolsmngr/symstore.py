'''
Created on 27.03.2013
    HB! :)
@author: capone
'''
import urlparse
import logging

from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter
from crashtec.utils.exceptions import CtGeneralError
from crashtec.utils.exceptions import CtBaseException

import dbmodel
import symstoredetails
import definitions
import downloader

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

class SymbolsStore(object):
    # Add's binaries to symbol store.
    # param urls_list - a list of url to zip files with binary data. 
    def add_binaries_from_urls(self, urls_list):
        for url in urls_list:
            try:
                self._add_single_url(url)
            except CtBaseException as e:
                _logger.error("Can't add url %s to symbols table. Exception message: %s", url, e)
           
    def _add_single_url(self, url):
        # Lookup current url in binary database
        result = _select_binary_by_url(url)
        if (result):
            _logger.info("detected binary dir: %s", result.local_dir)
            self._add_existing_binary_path(result)
            continue
            # So SYMBOLS_TRANSACTION_ID are not registred in db
            binaryDirrectory = downloader.download_and_unzip_url(url)
            if (not binaryDirrectory):
#                continue;
#            binaryDirrectory = definitions.convertToNetworkPath(binaryDirrectory)
#            # update itv symbols store
#            transactionId = symbolsStoreProvider.add_binary_to_symbol_store(binaryDirrectory)
#            if not transactionId:
#                return
#            #update database
#            dbUtils.addBinary(url, binaryDirrectory, transactionId, databaseCursor)
#    
    def _add_existing_binary_path(self, binary):
        d = dbmodel;
        if (binary[d.SYMBOLS_TRANSACTION_ID] != definitions.EMPTY_TRANSACTION):
            # Binary is already in symstore
            return
        _logger.info("Binary is not added to symbol store. Adding...")
        binary[d.SYMBOLS_TRANSACTION_ID] = symstoredetails.add_binary_to_symbol_store(binary.local_dir)
        dbroutines.update_record(d.SYMBOLS_TABLE, binary)
        _logger.info("Binary successfully added to symbol store")


# Returns BinaryRecord instance  
def _select_binary_by_url(binary_url):
    parsed_url = urlparse.urlparse(binary_url)
    if (not parsed_url):
        raise CtGeneralError("Could not parse url for request binary location on db: %s" % binary_url)
    d = dbmodel
    f = filter.FieldFilterFactory
    cursor = dbroutines.select_from(d.SYMBOLS_TABLE, filter = f(d.SYMBOLS_URL) == parsed_url.path)
    return cursor.fetchone()
