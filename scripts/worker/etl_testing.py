import logging
from sys import argv
from os import path

class Logger:
    """
    Monitors error/exceptions, listens for schedulers events and logs the same
    """
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG
    INFO = logging.INFO

    def __init__(self, threshold_level=logging.CRITICAL):
        """

        """
        self.threshold_level = threshold_level
        self.logger = self._get_logger()

    def log(self, log_message, level=logging.CRITICAL, source='', sourceUrl='http://localhost', exception=''):
        """
        Logs messages based on the specified level.
        """
        extra = {
            'source': source,
            'sourceUrl': sourceUrl,
            'exception': exception
        }
        self.logger.log(level, log_message, extra=extra)

    def _get_logger(self):
        script_name = path.basename(argv[0])
        logger = logging.getLogger(script_name)
        if not logger.hasHandlers():
            logger = logging.getLogger(script_name)
            console_handler = logging.StreamHandler()
            logger.setLevel(self.threshold_level)
            # console_handler.setLevel(self.threshold_level)
            # c_format = logging.Formatter('[%(levelname)s]  - %(name)s - %(message)s - %(asctime)s')
            # console_handler.setFormatter(c_format)
            # Add handlers to the logger
            # logger.addHandler(console_handler)
            log_fmt = ('time=%(asctime)s level="%(levelname)s" loggerName=%(name)s '
                       'message="%(message)s"  exception="%(exception)s"')
            c_format = logging.Formatter(log_fmt, datefmt="%Y-%m-%dT%H:%M:%S%z")
            console_handler.setFormatter(c_format)
            logger.addHandler(console_handler)
        return logger


if __name__ == '__main__':
    print(1)
