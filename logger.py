from logging import getLogger, handlers, Formatter, StreamHandler, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os
import sys


def setLogger(
    *,
    inFileLogLevel: str = 'INFO',
    inConsoleLogLevel: str = 'INFO',
    inLogName: str = 'app'
):
    # get root logger
    lRootLogger = getLogger()
    lRootLogger.setLevel(NOTSET)

    # remove existing handlers
    if lRootLogger.hasHandlers():
        lRootLogger.handlers.clear()

    # generate console handler
    lConsoleHandler = StreamHandler(sys.stdout)

    # generate rotating file handler
    log_file_path = os.path.join(os.path.dirname(
        __file__), 'log', inLogName + '.log')
    lRotatingHandler = handlers.RotatingFileHandler(
        log_file_path,
        mode="a",
        maxBytes=100 * 1024,
        backupCount=100,
        encoding="utf-8"
    )

    # set level
    lLevelDict = {
        'notset': NOTSET,
        'debug': DEBUG,
        'info': INFO,
        'warning': WARNING,
        'error': ERROR,
        'critical': CRITICAL
    }
    lConsoleHandler.setLevel(lLevelDict.get(inConsoleLogLevel.lower(), INFO))
    lRotatingHandler.setLevel(lLevelDict.get(inFileLogLevel.lower(), INFO))

    # set format
    lFormat = Formatter(
        '%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
    lRotatingHandler.setFormatter(lFormat)
    lConsoleHandler.setFormatter(lFormat)

    # add handlers
    lRootLogger.addHandler(lRotatingHandler)
    lRootLogger.addHandler(lConsoleHandler)
