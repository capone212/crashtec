'''
Created on 30.03.2013

@author: capone
'''
import unittest
import os
import shutil
import logging

from crashtec.symbolsmngr import symstore
from crashtec.db.provider import routines as dbroutines
from crashtec.utils import debug
from crashtec.symbolsmngr import dbmodel
from crashtec.symbolsmngr import definitions

def setup_log():
    logger = logging.getLogger('symbolsmngr')
    debug.init_debug_logger(logger)

TEMP_FOLDER = r'test_data\temp'
TEST_DATA_FOLDER = r'test_data\pdb'

def clean_temp_folder(folder):
    if (os.path.exists(folder)):
        shutil.rmtree(folder)
    os.makedirs(folder)

# TODO: check number of stored pointers and number of error's (optionaly)

class TestHttpDownloader(unittest.TestCase):        
    def test_add_binary_path(self):
        store = symstore.SymbolsStore(self, self.temp_dir)
        store.add_binary_path(self.test_data_dir)
    
    def setUp(self):
        self.temp_dir = os.path.join(os.path.dirname(__file__),
                                     TEMP_FOLDER)
        self.test_data_dir = os.path.join(os.path.dirname(__file__),
                                     TEST_DATA_FOLDER)
        clean_temp_folder(self.temp_dir)
    
    # SymstoreTable interface
    def select_binary_by_path(self, folder):
        self.assertTrue(folder, "Empty folder passed to SymstoreTable")
        record = dbroutines.Record()
        record[dbmodel.SYMBOLS_TRANSACTION_ID] = definitions.EMPTY_TRANSACTION
        return record
    
    def update_record(self, record):
        self.assertEqual(record[dbmodel.SYMBOLS_TRANSACTION_ID], '0000000001',
                         "Transaction id should not be empty")

setup_log()