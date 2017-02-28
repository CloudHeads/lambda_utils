# -*- coding: utf-8 -*-


__author__ = """CloudHeads"""
__email__ = 'theguys@cloudheads.io'
__version__ = '0.1.24'
import os
import logging


class Event(object):
    function = None
    wrapped_function = None

    @staticmethod
    def configure_logging():
        log_level = logging.INFO
        if os.environ.get('DEBUG', 'true').lower() == 'false':
            log_level = logging.ERROR
        logging.getLogger().setLevel(log_level)
        if os.environ.get('SENTRY_IO'):
            from raven.handlers.logging import SentryHandler
            from raven.transport.requests import RequestsHTTPTransport
            from raven.conf import setup_logging
            handler = SentryHandler(os.environ.get('SENTRY_IO'), transport=RequestsHTTPTransport, level=logging.ERROR)
            setup_logging(handler)

    def __call__(self, function):
        self.configure_logging()
        self.function = function
        return self.wrapped_function

    def wrapped_function(self, event, context):
        logging.info(event)
        response = self.function(event, context)
        logging.info(response)
        return response
