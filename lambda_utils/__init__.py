# -*- coding: utf-8 -*-
__author__ = """CloudHeads"""
__email__ = 'theguys@cloudheads.io'
__version__ = '__version__ = '0.2.3''

import logging
from concurrent.futures import ThreadPoolExecutor
from response_handlers import BaseResponseHandler
from logger import BaseLogger


class LambdaProcessor:
    def __init__(self, response_handler=None, loggers=None):

        self.response_handler = response_handler or BaseResponseHandler()
        self.loggers = loggers or [BaseLogger()]

    def on_init(self, function):
        for logger in self.loggers:
            logger.on_init(function)

    def on_execution(self, event):
        logging.debug(event)

        for logger in self.loggers:
            logger.on_execution(event)
        return self.response_handler.on_execution(event)

    def on_response(self, response):
        logging.debug(response)
        return self.response_handler.on_response(response)

    def on_exception(self, ex):
        logging.exception(ex.message)
        return self.response_handler.on_exception(ex)

    def __call__(self, function):
        self.on_init(function)
        self.function = function
        return self.wrapped_function

    def seconds_until_timeout(self, context):
        if hasattr(context, 'get_remaining_time_in_millis'):
            seconds = (context.get_remaining_time_in_millis() / 1000.00) - 1.0
            return seconds
        else:
            logging.debug('Add logging on timeout failed. context.get_remaining_time_in_millis() missing?')

    def wrapped_function(self, event, context):
        try:
            event = self.on_execution(event)
            timer = ThreadPoolExecutor(max_workers=1).submit(self.function, event, context)
            response = timer.result(timeout=self.seconds_until_timeout(context))
            return self.on_response(response)
        except Exception as ex:
            return self.on_exception(ex)
