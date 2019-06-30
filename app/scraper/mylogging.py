"""
    mylogging.py
    utility to set up logging
"""
import logging

LOGNAME = "scraper"

def init(loglevel=logging.DEBUG):
    """
        Creates standard logging
        for LOGNAME
    """
    logger = logging.getLogger(LOGNAME)
    logger.setLevel(logging.DEBUG)
    channel = logging.StreamHandler()
    channel.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    channel.setFormatter(formatter)
    logger.addHandler(channel)
    logger.debug("Initialized logging for %s", LOGNAME)

    return logger

# end
