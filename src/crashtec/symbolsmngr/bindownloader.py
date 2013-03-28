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
from crashtec.config import symbolsmngrconfig
import unzipBinaries

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

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
