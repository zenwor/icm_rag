import sys

import logging

general_format = "%(levelname)s - %(filename)s (%(funcName)s): %(message)s"
logging.basicConfig(level=logging.INFO, format=general_format)

log_enabled = True

def set_log_enabled(flag: bool):
    global log_enabled
    log_enabled = flag


def set_log_file(log_file: str):
    if log_file is not None:
        logger = logging.getLogger()
        logger.handlers = []
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(general_format))
        
        logger.addHandler(file_handler)
        
        
def log_info(msg):
    if log_enabled:
        logging.info(msg)
        
        
def log_warning(msg):
    if log_enabled:
        logging.warning(msg)
        

def log_error(msg):
    if log_enabled:
        logging.error(msg)    
        sys.exit("")
    
def log_debug(msg):
    if log_enabled:
        logging.debug(msg)
        
        
def log_critical(msg):
    if log_enabled:
        logging.critical(msg)