# -*- coding: utf-8 -*-

import os
import logging


class Logger(object):
    def configure_logging(self):
        log_level = getattr(logging, os.environ.get('LOGLEVEL', 'INFO').upper())
        logging.getLogger().setLevel(log_level)

    def __call__(self, function):
        self.configure_logging()
        self.function = function
        return self.wrapped_function

    def wrapped_function(self, event, context):
        logging.debug(event)
        response = self.function(event, context)
        logging.debug(response)
        return response
