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

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

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
            raise CtCriticalError("Could not parse url: %s" % safe_log_url(binary_url))
    

class StorageProvider(object):
    # Returns directory where binary may be placed
    # the path is unique for passed url 
    # and guarantied to be empty (at least for first time).
    # Throws on error.
    def create_place_for_binary(self, binary_url):
        pass
    #TODO: write it down
    
class HttpDownloader(object):
    # Downloads specified url to destination folder.
    # Returns downloaded file path, throws on error.
    def download_binary(self, url, destination_path):
        pass

class ZipUnpacker(object):
    # Unpacks specified binary package and returns destination folder.
    # Throws on errors.
    def unpack(self, package_file):
        pass


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
        _logger.debug("Processing binary url finished : %s", safe_log_url(url))
        return unpacked_binaries_folder
        
        

def reportHook(downloaded, blockSize, totalFileSize):
    percents = (downloaded * 100) / (totalFileSize / blockSize)
    _logger.info("downloaded %s\%", percents)
    

def downloadUrlToFile(url, toFile):
    timeOut = socket.getdefaulttimeout()
    result = None
    try:
        socket.setdefaulttimeout(10)
        result = urllib.urlretrieve(url, toFile, reportHook);
    except Exception as exc:
        _logger.warning("Failed download %s error: %s", url, str(exc))
    finally:
        socket.setdefaulttimeout(timeOut)
    if result:
        return toFile;
 
def createPlaceForUrl(url):
    parsedUrl = urlparse.urlparse(url)
    if (not parsedUrl):
        _logger.error("Could not parse url for obtain local binary location : %s", url)
        return
    
    dirrectory = symbolsmngrconfig.BINARY_LOCAL_ROOT + os.path.dirname(parsedUrl.path) 
    try:
        if (not os.path.exists(dirrectory)):
            os.makedirs(dirrectory) 
    except OSError as err:
        _logger.warning("error while creating dirrectory: %s", str(err)) 
    return os.path.join(dirrectory, os.path.basename(parsedUrl.path)) 

def downloadUrl(url):
    if (not url):
        return str()
    fileName = createPlaceForUrl(url)
    _logger.info("Downloading %s to file %s", url, fileName)
    result = downloadUrlToFile(url, fileName)
    if result : 
        _logger.info("Downloaded successfully %s", fileName)
    else:
        _logger.warning("Failed to download from: %s", url)
    return result
            
def download_and_unzip_url(url):
    zipFile = downloadUrl(url)
    if zipFile:
        _logger.info("Unzipping file %s....", zipFile)
        binaryDirrectory = unzipBinaries.unzipBinary(zipFile)
        # drop zip file 
        os.remove(zipFile)
        return binaryDirrectory
