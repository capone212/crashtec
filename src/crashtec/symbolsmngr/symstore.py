'''
Created on 27.03.2013
    HB! :)
@author: capone
'''
import logging

from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter
from crashtec.config import symbolsmngrconfig
import dbmodel
import symstoredetails
import definitions

_logger = logging.getLogger("symbolsmngr")


class SymstoreTable(object):
    def select_binary_by_path(self, folder):
        d = dbmodel
        f = filter.FieldFilterFactory
        cursor = dbroutines.select_from(d.SYMBOLS_TABLE, 
                            db_filter = f(d.SYMBOLS_LOCAL_DIR) == folder)
        return cursor.fetchone()
    
    def update_record(self, record):
        dbroutines.update_record(dbmodel.SYMBOLS_TABLE, record)

class SymbolsStore(object):
    def __init__(self, symtable, 
                 config = symbolsmngrconfig):
        self.symtable = symtable
        self.config = config
        #symbolsmngrconfig.SYMBOLS_STORE_LOCAL_DIR
    
    def add_binary_path(self, folder, task):
        record = self.symtable.select_binary_by_path(folder)
        d = dbmodel;
        if (record[d.SYMBOLS_TRANSACTION_ID] != definitions.EMPTY_TRANSACTION):
            # Binary is already in symstore
            _logger.info("Binary is already in symbol store.")
            return
        _logger.info("Adding binary to symbol store...")
        record[d.SYMBOLS_TRANSACTION_ID] = \
            symstoredetails.add_binary_to_symbol_store(folder, 
                                        self.config.SYMBOLS_STORE_LOCAL_DIR,
                                        task[d.TASKS_PLATFORM_FIELD])
        self.symtable.update_record(record)
        _logger.info("Binary successfully added to symbol store.")
    