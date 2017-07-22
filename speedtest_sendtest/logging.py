import logging
import os


def create_logger():
    """
    Sets up logging
    :returns logging object named log
    """
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger(__name__)
    return log
