#!/usr/bin/python

import os
import sys
import logging
import logging.handlers

def start_logging(filename=None, debug=False, quiet=False):
    # set defaults
    format = ['%(message)s']
    level = logging.INFO
    file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=1000*1024, backupCount=9)
    
    # set debug options
    if debug:
        format = ['%(asctime)-15s %(levelname)-8s %(name)-11s %(message)s', '%Y-%m-%d %H:%M']
        level = logging.DEBUG
        file_handler = logging.StreamHandler()
    
    # root logger
    logger = logging.getLogger()
    
    # set the log format.
    formatter = logging.Formatter(*format)
    
    mem_handler = logging.handlers.MemoryHandler(1000*1000, 100)
    mem_handler.setFormatter(formatter)
    logger.addHandler(mem_handler)
    
    file_handler.setFormatter(mem_handler.formatter)
    
    mem_handler.setTarget(file_handler)
    
    logger.removeHandler(mem_handler)
    logger.addHandler(file_handler)
    
    logger.setLevel(level)
    
    if not debug and not quiet:
        console = logging.StreamHandler()
        console.setFormatter(file_handler.formatter)
        logger.addHandler(console)
        
        # flush memory handler to the console without destroying the buffer
        if len(mem_handler.buffer) > 0:
            for record in mem_handler.buffer:
                console.handle(record)
    
    # flush what we have stored from the module initialization
    mem_handler.flush()
