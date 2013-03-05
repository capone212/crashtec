'''
Created on 06.03.2013

@author: capone
'''
import logging
import sys

def init_debug_logger(logger):
    # Set Log level
    logger.setLevel(logging.DEBUG)
    #Set handler11111
    log_handler = logging.StreamHandler(sys.stdout)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)