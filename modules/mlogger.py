#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'werewolfLu'

import inspect
import os
import tempfile
import logging
from logging.handlers import RotatingFileHandler


def init_rotatefilelog():
    log_formatter = logging.Formatter('%(asctime)s [%(process)d] %(funcName)s(%(lineno)d) %(message)s')
    logFile = os.path.join(tempfile.gettempdir(), "aicanteen_baiduapi.log")
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5 * 1024 * 1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    app_log = logging.getLogger()
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)
    return app_log


def init_consolelogging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(process)d] %(funcName)s(%(lineno)d) %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))
    return logger


def get_caller_function():
    (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
    return function_name


def get_caller_info_total():
    frame_info = (frame, filename, line_number, function_name, lines, index) = \
    inspect.getouterframes(inspect.currentframe())[0]
    return frame_info


def get_caller_info(frames=None):
    if not frames:
        frames = len(inspect.getouterframes(inspect.currentframe()))
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[frames - 1]
    else:
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[frames]
    print(frame, filename, line_number, function_name, lines, index)
    return filename


mlogger = init_rotatefilelog()
# mlogger = init_consolelogging()


if __name__ == "__main__":
    v = 1
    d = {'a':1}
    mlogger.debug("test %s, %s", v, d)