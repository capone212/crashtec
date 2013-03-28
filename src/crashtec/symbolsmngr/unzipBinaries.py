import zipfile, os, re
import logging
gLogger = logging.getLogger("symbolsmngr.symbolsmngr")

# TODO: Style!!!


def getPlaceForUnzipFile(filename):
    pattern = "(.+).zip"
    matchObj = re.match(pattern, filename)
    if (not matchObj):
        gLogger.info("Could not parse filename for obtain local binary location:%s", filename)
        return
    dirrectory = matchObj.group(1); 
    try:
        if (not os.path.exists(dirrectory)):
            os.makedirs(dirrectory) 
    except OSError as err:
        gLogger.error("Error while creating dirrectory: %s", err) 
    return dirrectory + "/"

def unzipBinary(filename):
    if (not filename):
        gLogger.error("invalid parameter in unzipBinary: %s", unzipBinary)
        return
    # Check zip file
    if (not zipfile.is_zipfile(filename)):
        gLogger.error("Error: input path is not zip file: %s", filename)
        return
    #Create dirrectory for unzip
    dirrectory = getPlaceForUnzipFile(filename)
    if not dirrectory:
        return 
    #Unzip
    try:
        zip = zipfile.ZipFile(filename)
        zip.extractall(dirrectory)
        zip.close()
        return dirrectory
    except zipfile.BadZipfile as err:
        gLogger.error("Could not decompress zip file %s exception: %s", filename, err)
    except zipfile.LargeZipFile as err:
        gLogger.error("Could not decompress zip file %s exception: %s", filename, err)
