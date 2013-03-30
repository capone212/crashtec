'''
Created on 30.03.2013

@author: capone
'''

import unittest
import os
import shutil
import logging

from crashtec.symbolsmngr import bindownloader
from crashtec.utils import debug
from crashtec.utils.exceptions import CtBaseException

TEMP_FOLDER = 'test_data/temp'
TEST_DATA_FOLDER = 'test_data'

def clean_temp_folder(folder):
    if (os.path.exists(folder)):
        shutil.rmtree(folder)
    os.makedirs(folder)
    
def setup_log():
    logger = logging.getLogger('symbolsmngr')
    debug.init_debug_logger(logger)

class TestHttpDownloader(unittest.TestCase):        
    def test_download_binary_file_exists(self):
        #TODO: enable me
        return
        http = bindownloader.HttpDownloader()
        source_url = "http://download.thinkbroadband.com/5MB.zip"
        file_name = http.download_binary(source_url, self.temp_dir)
        self.assertTrue(os.path.exists(file_name), 
                        "Can't located downloaded file.")
        file_info = os.stat(file_name)
        self.assertEqual(file_info.st_size, 5 * 1024 * 1024, 
                         "Downloaded file does not have correct size")
    
    def test_download_binary_file_is_absent(self):
        http = bindownloader.HttpDownloader()
        source_url = "http://ya.sample.uu/5MB.zip"
        with self.assertRaises(CtBaseException):
            http.download_binary(source_url, self.temp_dir)
    
    def setUp(self):
        self.temp_dir = os.path.join(os.path.dirname(__file__), TEMP_FOLDER)
        clean_temp_folder(self.temp_dir)
    
    @classmethod 
    def setUpClass(cls):
        setup_log()

class TestStorageProvider(unittest.TestCase):
    def test_create_place_for_binary(self):
        first_url = "https://al:pass@thinkbroadband.com/pdb-23/5MB.zip"
        second_url = "https://al:pass@thinkbroadband.com/pdb-24/5MB.zip"
        storage = bindownloader.StorageProvider()
        first_dir = storage.create_place_for_binary(first_url)
        second_dir = storage.create_place_for_binary(second_url)
        self.assertTrue(first_dir)
        self.assertTrue(second_dir)
        self.assertNotEquals(first_dir, second_dir, "Two folders path should be different")
        #shutil.rmtree(first_dir)
        #shutil.rmtree(second_dir)

class TestZipUnpacker(unittest.TestCase):
    def test_correct_zip(self):
        unpacker = bindownloader.ZipUnpacker()
        path = unpacker.unpack(os.path.join(self.testdata_dir, 'correct.zip'),
                               self.temp_dir)
        result = os.path.exists(os.path.join(path, 'correct'))
        self.assert_(result, "Can't locate unzipped file!")
    
    def test_corrupted_zip(self):
        unpacker = bindownloader.ZipUnpacker()
        with self.assertRaises(CtBaseException):
            unpacker.unpack(os.path.join(self.testdata_dir, 'bad.zip'),
                               self.temp_dir)
        
    
    def setUp(self):
        self.temp_dir = os.path.join(os.path.dirname(__file__), TEMP_FOLDER)
        self.testdata_dir = os.path.join(os.path.dirname(__file__),
                                         TEST_DATA_FOLDER, "zip")
        clean_temp_folder(self.temp_dir)



