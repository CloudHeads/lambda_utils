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
        timer = self.add_logging_on_timeout(event, context)
        try:
            logging.debug(event)
            response = self.function(event, context)
            logging.debug(response)
            return response
        except Exception as ex:
            logging.exception(ex.message)
            raise
        finally:
            if timer: timer.cancel()

    def timeout_notification(self, event, context, **kwargs):
        logging.error('Execution is about to timeout.', **kwargs)

    def add_logging_on_timeout(self, event, context):
        if hasattr(context, 'get_remaining_time_in_millis'):
            seconds = (context.get_remaining_time_in_millis() / 1000.00) - 0.5
            timer = threading.Timer(seconds, self.timeout_notification, args=[event, context])
            timer.start()
            return timer
        else:
            logging.debug('Add logging on timeout failed. context.get_remaining_time_in_millis() missing?')
