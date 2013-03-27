'''
Created on 27.03.2013
    HB! :)
@author: capone
'''
import urllib
import os
import socket
import definitions
import urlparse
import logging

_logger = logging.getLogger("symbolsmngr.symbolsmngr")

def reportHook(downloaded, blockSize, totalFileSize):
    percents = (downloaded * 100) / (totalFileSize / blockSize)
    _logger.info("downloaded %s\%", percents)
    

def downloadUrlToFile(url, toFile):
    timeOut = socket.getdefaulttimeout()
    result = None
    try:
        socket.setdefaulttimeout(10)
        result = urllib.urlretrieve(url, toFile);#, reportHook);
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
    
    dirrectory = definitions.BINARY_LOCAL_ROOT + os.path.dirname(parsedUrl.path) 
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
            
def downloadAndUnzipUrl(url):
    zipFile = downloadUrl(url)
    if zipFile:
        _logger.info("Unzipping file %s....", zipFile)
        binaryDirrectory = unzipBinaries.unzipBinary(zipFile)
        # drop zip file 
        os.remove(zipFile)
        return binaryDirrectory

def addExistBinaryToSymStore(binary, databaseCursor):
    if (binary.symstore_transaction_id != dbUtils.EMPTY_TRANSACTION):
        return
    _logger.info("Binary is not added to symbol store. Adding...")
    transactionId = symbolsStoreProvider.add_binary_to_symbol_store(binary.local_dir)
    if not transactionId:
        _logger.warning("Error: Could not add dir to symbols store")
        return
    dbUtils.updateTransactionIdForBinary(binary.local_dir, transactionId, databaseCursor)
    _logger.info("Binary successfully added to symbol store")

def addBinariesPathsFromUrlListToSymbolStore(urlList, databaseCursor):    
    binaryDirrectoryList = []
    for url in urlList:
        #look ahead in binary database
        result = dbUtils.requestBinaryByPath(url, databaseCursor)
        if (result):
            binaryDirrectoryList.append(result.local_dir)
            _logger.info("detected binary dir: %s", result.local_dir)
            addExistBinaryToSymStore(result, databaseCursor)
            continue
        #download binary if there are not registred in db
        binaryDirrectory = downloadAndUnzipUrl(url)
        if (not binaryDirrectory):
            continue;
        binaryDirrectory = definitions.convertToNetworkPath(binaryDirrectory)
        # update itv symbols store
        transactionId = symbolsStoreProvider.add_binary_to_symbol_store(binaryDirrectory)
        if not transactionId:
            return
        #update database
        dbUtils.addBinary(url, binaryDirrectory, transactionId, databaseCursor)
        binaryDirrectoryList.append(binaryDirrectory)
    return binaryDirrectoryList
        

#urlList = ["https://anzor.apshev:sDWzgu212@msk.itvgroup.ru/bamboo/browse/DTP-DEF30-6/artifact/Binaries/ItvDetectorPack_bin.zip",
#           "https://anzor.apshev:sDWzgu212@msk.itvgroup.ru/bamboo/browse/DTP-DEF30-6/artifact/msi/DetectorPackInstaller.msi",
#           "https://anzor.apshev:sDWzgu212@msk.itvgroup.ru/bamboo/browse/DTP-DEF30-6/artifact/pdb/ItvDetectorPack_pdb.zip" 
#           ]
#result = addBinariesPathsFromUrlListToSymbolStore(urlList)
#print(result)
