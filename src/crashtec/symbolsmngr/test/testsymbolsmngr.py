'''
Created on 07.04.2013

@author: capone
'''
import unittest
from mock import MagicMock
from mock import patch
import mock
import logging

from crashtec.utils.exceptions import CtGeneralError
from crashtec.symbolsmngr.bindownloader import BinaryDownloader
from crashtec.symbolsmngr.symstore import SymbolsStore
from crashtec.symbolsmngr import symbolsmngr

from crashtec.utils import debug 

_sample_task = dict()
_sample_products_list = {'prod1' : ['1.0.0.', '1.0.2']}
_sample_urls = ['url1', 'url2']
_binary_folder_list = ['folder1', 'folder2']

class MocSymbolsManagerBuilder(object):
    
    def __init__(self):
        self.agent_class = 'agent_class'
        self.instance_name = 'instance_name'
    
    def build_products_detector(self):
        self.products_detector = MagicMock(
                        spec_set = ['get_products_list_for_task']) 
        
        self.products_detector.get_products_list_for_task = MagicMock(
            return_value = _sample_products_list)
        
        return self
    
    def build_binaries_locator(self):
        self.binaries_locator = MagicMock(
                                spec_set = ['get_binaries_url_for_products'])
        self.binaries_locator.get_binaries_url_for_products = MagicMock(
                                            return_value = _sample_urls)
        return self
    
    def build_downloader(self):
        self.downloader = mock.create_autospec(BinaryDownloader, spec_set=True)
        self.downloader.download_and_unpack.side_effect = _binary_folder_list
        return self
    
    def build_symbols_store(self):
        self.symbols_store = mock.create_autospec(SymbolsStore, spec_set = True)
        #self.symbols_store.add_binary_path.return_value = 10
        #self.symbols_store.add_binary_path = mock.mocksignature(
        #                    SymbolsStore.add_binary_path, skipfirst=True)
        return self
    
    def create(self):
        impl = symbolsmngr.Implementation(self.products_detector,
                                          self.binaries_locator,
                                          self.downloader,
                                          self.symbols_store)
        return symbolsmngr.SymbolsManager(impl, self.agent_class,
                                          self.instance_name)

class MocBuilderProductDetectorThrows(MocSymbolsManagerBuilder):
    def build_products_detector(self):
        self.products_detector = MagicMock(
                        spec_set = ['get_products_list_for_task']) 
        
        self.products_detector.get_products_list_for_task = MagicMock(
            side_effect = CtGeneralError('Mock intended error')) 
        return self

class MocBuilderSymbolsStoreThrows(MocSymbolsManagerBuilder):
    def build_symbols_store(self):
        self.symbols_store = MagicMock(spec_set = SymbolsStore)
        self.symbols_store.add_binary_path = MagicMock(
            side_effect = CtGeneralError('Mock intended error')) 
        return self


@patch('crashtec.infrastructure.public.agentbase.RegistrationHolder')
class TestSymbolsManager(unittest.TestCase): 
    # Here we should not have any errors. It is just regular success path.
    def test_task_success(self, mock_class):
        self._test_task_success(mock_class, MocSymbolsManagerBuilder())
        
    def _test_task_success(self, mock_class, builder):
        # Setup mock's
        manager = self.build_mock(builder)
        manager.task_failed = MagicMock(side_effect = 
                                        RuntimeError("Should not be called"))
        
        # Call
        manager.process_task(_sample_task)
        
        # Validate call's
        impl = manager.impl 
        impl.products_detector.get_products_list_for_task.\
                        assert_called_once_with(_sample_task)
        impl.binaries_locator.get_binaries_url_for_products.\
                        assert_called_once_with(_sample_products_list, 
                                                _sample_task)
        download_calls = [mock.call(url) for url in _sample_urls]
        impl.downloader.download_and_unpack.assert_has_calls(download_calls, 
                                                        any_order=True)
        folder_calls = [mock.call(folder, _sample_task) 
                        for folder in _binary_folder_list]
        impl.symbols_store.add_binary_path.assert_has_calls(folder_calls,
                                                        any_order=True)
        manager.task_finished.assert_called_once_with(_sample_task)
    
    # Here task should fail, because  manager could not find products
    def test_products_detector_throws(self, mock_class):
        manager = self.build_mock(MocBuilderProductDetectorThrows())
        manager.task_finished = MagicMock(side_effect = 
                                        RuntimeError("Should not be called"))
        # Call
        manager.process_task(_sample_task)
        # Validate call's
        manager.task_failed.assert_called_once_with(_sample_task)
    
    # Here we have exceptions at adding to symbols store, but
    # there are many folders to add, so failing at one item should not
    # lead to failing all the task   
    def test_symbolsstore_throws(self, mock_class):
        manager = self.build_mock(MocBuilderSymbolsStoreThrows())
        manager.task_failed = MagicMock(side_effect = 
                                        RuntimeError("Should not be called"))
        # Call
        manager.process_task(_sample_task)
        # Validate call's
        download_calls = [mock.call(url) for url in _sample_urls]
        manager.impl.downloader.download_and_unpack.assert_has_calls(
                                    download_calls, any_order=True)
        manager.task_finished.assert_called_once_with(_sample_task)
        
    def build_mock(self, builder):
        manager = builder.build_products_detector().\
                build_binaries_locator().\
                build_downloader().\
                build_symbols_store().create()
            
        manager.task_failed = MagicMock()
        manager.task_finished = MagicMock()
        return manager


def setup_log():
    logger = logging.getLogger('symbolsmngr')
    debug.init_debug_logger(logger)

setup_log()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()