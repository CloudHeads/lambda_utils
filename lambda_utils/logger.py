# -*- coding: utf-8 -*-

import os
import logging
import threading


class Logger(object):
    def configure_logging(self):
        log_level = getattr(logging, os.environ.get('LOGLEVEL', 'INFO').upper())
        logging.getLogger().setLevel(log_level)

    def __call__(self, function):
        self.configure_logging()
        self.function = function
        return self.wrapped_function

    def wrapped_function(self, event, context):
        try:
            timeout_notification = self.add_logging_on_timeout(context)
            logging.debug(event)
            response = self.function(event, context)
            logging.debug(response)
            return response
        except Exception as ex:
            logging.exception(ex.message)
            raise
        finally:
            if timeout_notification: timeout_notification.cancel()

    def add_logging_on_timeout(self, context):
        try:
            timer = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5, timeout)
            timer.start()
            return timer

        except AttributeError as ex:
            logging.debug('Add Timeout notification failed. context.get_remaining_time_in_millis() missing?')


def timeout():
    logging.error("Execution is about to timeout.")
