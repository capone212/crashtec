'''
Created on 17.02.2013

@author: capone
'''

import platform
#import socket


def get_host_name():
    # NOTE:  socket.gethostname() is also acceptable
    return platform.node()