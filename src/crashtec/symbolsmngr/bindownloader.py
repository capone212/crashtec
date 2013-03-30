'''
Created on 27.03.2013
    HB! :)
@author: capone
'''
# TODO: Style!!! rewrite it all

import urllib
import os
import socket
import urlparse
import logging
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter
from crashtec.config import symbolsmngrconfig
from crashtec.utils.exceptions import CtGeneralError
from crashtec.utils.exceptions import CtCriticalError

import unzipBinaries
import dbmodel
import definitions

_logger = logging.getLogger('symbolsmngr')

# TODO: write unit tests!!!!!!!!!!! it should be easy

# Strips dangerous (like authentication info) 
def safe_log_url(url):
    return url

class Cache(object):
    def __init__(self, instance_name):
        self.agent_name = instance_name
        
    # Returns appropriate directory path if specified url in cache,
    # returns None otherwise. 
    def lookup_binary_path(self, binary_url):
        d = dbmodel
        f = filter.FieldFilterFactory
        stripped_url = self.strip_url(binary_url)
        cursor = dbroutines.select_from(d.SYMBOLS_TABLE, filter = (
                                        (f(d.SYMBOLS_URL) == stripped_url) &
                                        (f(d.SYMBOLS_AGENT_ID) == self.agent_name))
                                        ) 
        record = cursor.fetchone()
        if record:
            return record[d.SYMBOLS_LOCAL_DIR]
    
    # Makes new record in cache
    # Throws on error.
    def register_binary(self, url, binary_dirrectory):
        stripped_url = self.strip_url(url)
        record = dbroutines.Record()
        d = dbmodel
        record[d.SYMBOLS_TRANSACTION_ID] = definitions.EMPTY_TRANSACTION
        record[d.SYMBOLS_URL] = stripped_url
        record[d.SYMBOLS_AGENT_ID] = self.agent_name
        record[d.SYMBOLS_LOCAL_DIR] = binary_dirrectory
        dbroutines.create_new_record(d.SYMBOLS_TABLE, record)
        
    # Strip's all unpersistent (like server address) info from url.
    def strip_url(self, binary_url):
        parsed_url = urlparse.urlparse(binary_url)
        if (not parsed_url):
            raise CtCriticalError("Could not parse url: %s" %
                                   safe_log_url(binary_url))
        return parsed_url.path
    

class StorageProvider(object):
    # Returns directory where binary may be placed
    # the path is unique for passed url 
    # and guarantied to be empty (at least for first time).
    # Throws on errors.
    def create_place_for_binary(self, binary_url):
        parsed_url = urlparse.urlparse(binary_url)
        if (not parsed_url):
            raise CtCriticalError("Could not parse url: %s" %
                                   safe_log_url(binary_url))
        
        dirrectory = symbolsmngrconfig.BINARY_LOCAL_ROOT + parsed_url.path
        try:
            if (not os.path.exists(dirrectory)):
                os.makedirs(dirrectory) 
        except OSError as err:
            raise CtGeneralError("Error while creating dirrectory: %s" % err) 
        return dirrectory
    
class HttpDownloader(object):
    # Downloads specified url to destination folder.
    # Returns downloaded file path, throws on error.
    def download_binary(self, url, dest_folder):
        self.reset_state()
        time_out = socket.getdefaulttimeout()
        parsed_url = urlparse.urlparse(url)
        file_name = os.path.join(dest_folder, os.path.basename(parsed_url.path))
        try:
            socket.setdefaulttimeout(10)
            result = urllib.urlretrieve(url, file_name, self.reportHook);
        except Exception as exc:
            raise CtGeneralError("Failed to download %s error: %s" % (url, exc))
        finally:
            socket.setdefaulttimeout(time_out)
        return file_name
    
    def reset_state(self):
        self._percents = 0;
    
    def reportHook(self, downloaded, blockSize, totalFileSize):
        blocks_amount = totalFileSize / blockSize
        if (blocks_amount == 0):
            return
        percents = (downloaded * 100) / blocks_amount
        # report every X percent downloaded
        REPORT_EACH_PERCENT = 10
        percents = (percents / REPORT_EACH_PERCENT) * REPORT_EACH_PERCENT;
        if (percents !=  self._percents):
            _logger.info("Downloaded %s%%", percents)
            self._percents = percents
        

class ZipUnpacker(object):
    # Unpacks specified binary package and returns destination folder.
    # Throws on errors.
    def unpack(self, package_file, destination):
        _logger.info("Unzipping binary %s ..." % package_file)
        binary_dirrectory = unzipBinaries.unzipBinary(package_file, destination)
        if (not binary_dirrectory):
            raise CtGeneralError("Can't extract zip file %s" % package_file)
        return binary_dirrectory


class BinaryDownloader(object):
    def __init__(self, cache, storage, downloader, unpacker):
        self.cache = cache
        self.storage = storage
        self.downloader = downloader
        self.unpacker = unpacker
    
    # Downloads binaries from url, unpack them and return 
    # destination directory.
    def download_and_unpack(self, url): 
        # Lookup cache for binary first.
        cached_path = self.cache.lookup_binary_path(url)
        if cached_path:
            _logger.info("Detected binary dir: %s", cached_path)
            return cached_path
        _logger.debug("Start processing binary url : %s", safe_log_url(url))
        destination_folder = self.storage.create_place_for_binary(url)
        package_file = self.downloader.download_binary(url, destination_folder)
        unpacked_binaries_folder = self.unpacker.unpack(package_file)
        self.drop_package_file(package_file)
        _logger.debug("Processing binary url finished : %s", safe_log_url(url))
        return unpacked_binaries_folder
    
    # Feel free to override it in subclasses
    def drop_package_file(self, package_file):
        # Delete package_file file 
        os.remove(package_file)
