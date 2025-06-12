import logging
def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    info_handler = logging.FileHandler("logs/info.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
    return logger

