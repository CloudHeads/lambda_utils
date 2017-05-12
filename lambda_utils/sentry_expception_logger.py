# -*- coding: utf-8 -*-
import os
import logging
from logger import Logger
from raven import Client
from raven.handlers.logging import SentryHandler
from raven.transport.requests import RequestsHTTPTransport
from raven.conf import setup_logging


class SentryExceptionLogger(Logger):
    def configure_logging(self):
        Logger.configure_logging(self)
        self.client = Client(dsn=os.environ['SENTRY_IO'], transport=RequestsHTTPTransport, name=os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
        self.handler = SentryHandler(client=self.client, level=logging.ERROR)
        setup_logging(self.handler)

    def add_user_context(self, event):
        try:
            user_context = {}
            for key, value in event['requestContext']['authorizer'].iteritems():
                user_context[key.lower()] = value
            self.client.user_context(user_context)
        except:
            logging.debug("No user  context recognized in event['requestContext']['authorizer']")

    def add_x_ray_tags(self, event):
        try:
            if os.environ.has_key('_X_AMZN_TRACE_ID'):
                self.client.tags_context({'X-Amzn-Trace-Id': os.environ['_X_AMZN_TRACE_ID']})

            request_trace_id = event['headers']['X-Amzn-Trace-Id']
            for trace_id in request_trace_id.split(';'):
                if 'Root' in trace_id or 'root' in trace_id:
                    self.client.tags_context({os.environ.get('SourceTraceId', 'Request-X-Amzn-Trace-Id'): trace_id})
        except:
            logging.debug("No request x-ray-trace-id recognized in event[u'headers'][u'X-Amzn-Trace-Id']")

    def wrapped_function(self, event, context):
        self.add_user_context(event)
        self.add_x_ray_tags(event)
        return Logger.wrapped_function(self, event, context)
