import json
import logging
import urllib2
from lambda_utils.response_handlers import BaseResponseHandler

FAILED = 'FAILED'
SUCCESS = 'SUCCESS'


class Cloudformation(BaseResponseHandler):
    def on_execution(self, event):
        try:
            self.event = json.loads(event['Records'][0]['Sns']['Message'])
        except:
            self.event = event
        return BaseResponseHandler.on_execution(self, event)

    def on_exception(self, ex):
        send_signal(self.event, FAILED, ex.message)
        BaseResponseHandler.on_exception(self, ex)


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
        },
        sort_keys=True,
    )
    logging.debug(response_body)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(event['ResponseURL'], data=response_body)
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', len(response_body))
    request.get_method = lambda: 'PUT'
    opener.open(request)
