'''
Created on 06.03.2013

@author: capone
'''
import logging
import sys
import datetime

from crashtec.infrastructure.public import agentutils 

def init_debug_logger(logger):
    # Set Log level
    logger.setLevel(logging.DEBUG)
    #Set handler11111
    log_handler = logging.StreamHandler(sys.stdout)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


def print_agent_log_header(logger, class_type, instance_name, 
                           group_id = agentutils.GROUP_ID_UNSET):
    logger.info('-'*40)
    logger.info('Agent instance name=%s  type=%s group_id=%s', 
                class_type, instance_name, group_id)
    logger.info('New run at %s', datetime.datetime.now())
    logger.info('-'*40)