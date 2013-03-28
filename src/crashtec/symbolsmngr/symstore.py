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
import bindownloader

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
    
    # Subclass this method you can override behavior. This may be useful 
    # if you want to work with network path's, use symbolic links and so on. 
    def convert_binary_path(self, binary_path):
        return binary_path
           
    def _add_single_url(self, url):
        # Lookup current url in binary database
        result = self._select_binary_by_url(url)
        if (result):
            _logger.info("detected binary dir: %s", result.local_dir)
            self._add_existing_binary_path(result)
            return
        # So this binary is not registered in db
        binary_dirrectory = bindownloader.download_and_unzip_url(url)
        if (not binary_dirrectory):
            raise CtGeneralError("Could create place for binary url: %s" % url)
        # update symbols store
        binary_dirrectory = self.convert_binary_path(binary_dirrectory)
        transaction_id = symstoredetails.add_binary_to_symbol_store(binary_dirrectory)
        self._make_binary_record_in_db(url, binary_dirrectory, transaction_id)
  
    def _add_existing_binary_path(self, binary):
        d = dbmodel;
        if (binary[d.SYMBOLS_TRANSACTION_ID] != definitions.EMPTY_TRANSACTION):
            # Binary is already in symstore
            return
        _logger.info("Binary is not added to symbol store. Adding...")
        binary[d.SYMBOLS_TRANSACTION_ID] = \
            symstoredetails.add_binary_to_symbol_store(binary.local_dir)
        dbroutines.update_record(d.SYMBOLS_TABLE, binary)
        _logger.info("Binary successfully added to symbol store")

    def _select_binary_by_url(self, binary_url):
        parsed_url = urlparse.urlparse(binary_url)
        if (not parsed_url):
            raise CtGeneralError("Could not parse url for request binary location on db: %s" % binary_url)
        d = dbmodel
        f = filter.FieldFilterFactory
        cursor = dbroutines.select_from(d.SYMBOLS_TABLE, filter = f(d.SYMBOLS_URL) == parsed_url.path)
        return cursor.fetchone()

    def _make_binary_record_in_db(self, url, binary_dirrectory, transaction_id):
        parsed_url = urlparse.urlparse(url)
        if (not parsed_url):
            raise CtGeneralError("Could not parse url for save binary location on db: %s" % url)
        record = dbroutines.Record()
        d = dbmodel
        record[d.SYMBOLS_TRANSACTION_ID] = transaction_id
        record[d.SYMBOLS_URL] = parsed_url.path
        record[d.SYMBOLS_LOCAL_DIR] = binary_dirrectory
        dbroutines.create_new_record(d.SYMBOLS_TABLE, record)
    