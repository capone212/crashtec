import zipfile
import logging
gLogger = logging.getLogger("symbolsmngr")

def unzipBinary(filename, dirrectory):
    if (not filename):
        gLogger.error("invalid parameter in unzipBinary: %s", unzipBinary)
        return
    # Check zip file
    if (not zipfile.is_zipfile(filename)):
        gLogger.error("Error: input path is not zip file: %s", filename)
        return
    #Unzip
    try:
        zip_file = zipfile.ZipFile(filename)
        zip_file.extractall(dirrectory)
        zip_file.close()
        return dirrectory
    except zipfile.BadZipfile as err:
        gLogger.error("Could not decompress zip file %s exception: %s", filename, err)
    except zipfile.LargeZipFile as err:
        gLogger.error("Could not decompress zip file %s exception: %s", filename, err)
