'''
Created on 15.03.2013

@author: capone
'''
import logging

from crashtec.infrastructure.public import agentbase
from crashtec.infrastructure.public import taskutils
from crashtec.utils.exceptions import CtBaseException

_logger = logging.getLogger("symbolsmngr")

class SymbolsManager(agentbase.AgentBase):
    def __init__(self, impl, class_type, instance_name, group_id):
        self.impl = impl
        agentbase.AgentBase.__init__(self, class_type, instance_name, group_id)
    
    def process_task(self, task):
        _logger.debug('About to start processing task: %s', 
                      taskutils.get_task_id(task))
        try:
            products_list = self.impl.get_products_list_for_task(task)
            binaries_url = self.impl.get_binaries_url_for_products(
                                                products_list, task)
            self._download_and_add(binaries_url, task)
            
            self.task_finished(task)
            _logger.debug('Task finished.')
        except CtBaseException as e:
            _logger.error('Exception occurred while processing task: %s', e)
            self.task_failed(task)
    
    def _download_and_add(self, urls_list, task):
        for url in urls_list:
            try:
                binaries_directory = self.impl.download_and_unpack(url)
                self.impl.add_symbols_to_store(binaries_directory, task)
            except CtBaseException as e:
                _logger.error('Exception occurred while processing url: %s', e)

class Implementation(object):
    def __init__(self, 
                 products_detector,
                 binaries_locator,
                 downloader,
                 symbols_store):
        self.products_detector = products_detector
        self.binaries_locator = binaries_locator
        self.downloader = downloader
        self.symbols_store = symbols_store
    
    def get_products_list_for_task(self, task):
        return self.products_detector.get_products_list_for_task(task)
    
    def get_binaries_url_for_products(self, products_versions, task):
        return self.binaries_locator.get_binaries_url_for_products(
                                        products_versions, task)
    
    def download_and_unpack(self, url):
        return self.downloader.download_and_unpack(url)
    
    def add_symbols_to_store(self, folder, task):
        return self.symbols_store.add_binary_path(folder, task)
    
