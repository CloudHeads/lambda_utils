# -*- coding: utf-8 -*-
import os
import logging
from raven.handlers.logging import SentryHandler
from raven.transport.requests import RequestsHTTPTransport
from raven.conf import setup_logging


class SentryExceptionLogger(object):
    def configure_logging(self):
        if os.environ.get('SENTRY_IO'):
            handler = SentryHandler(os.environ.get('SENTRY_IO'), transport=RequestsHTTPTransport, level=logging.ERROR)
            setup_logging(handler)

    def __call__(self, function):
        self.configure_logging()
        self.function = function
        return self.wrapped_function

    def wrapped_function(self, event, context):
        response = self.function(event, context)

        return response
