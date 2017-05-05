# -*- coding: utf-8 -*-
import json
import urllib2
import logging


class Cloudformation(object):
    def __call__(self, function):
        self.function = function
        return self.wrapped_function

    def wrapped_function(self, event, context):
        logging.info(event)
        self.event = self.extract_event(event)
        self.status = 'FAILED'
        self.response = None
        self.reason = None

        try:
            self.response = self.function(self.event, context)
            self.status = 'SUCCESS'
            return self.response
        except Exception as ex:
            logging.exception(ex.message)
            self.reason = ex.message
            raise
        finally:
            send_signal(self.event, self.status, self.reason, self.response)

    def extract_event(self, event):
        event = dict(event)
        # SNS Topic to Custom Resource
        if 'Records' in event:
            event = json.loads(event['Records'][0]['Sns']['Message'])
        return event


def send_signal(event, response_status, reason, response_data=None):
    response_body = json.dumps(
        {
            'Status': response_status,
            'Reason': str(reason or 'ReasonCanNotBeNone'),
            'PhysicalResourceId': event.get('PhysicalResourceId', event['LogicalResourceId']),
            'StackId': event['StackId'],
            'RequestId': event['RequestId'],
            'LogicalResourceId': event['LogicalResourceId'],
            'Data': response_data or {}
        }
    )
    logging.info(response_body)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(event['ResponseURL'], data=response_body)
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', len(response_body))
    request.get_method = lambda: 'PUT'
    opener.open(request)
