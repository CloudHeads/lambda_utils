import json
import logging
import urlparse
from lambda_utils import Event
from lambda_utils.exceptions import HTTPException, HTTP_STATUS_CODES


class ApiGateway(Event):
    event = None
    headers = None
    code = None
    body = None

    def wrapped_function(self, event, context):
        self.event = dict(event)
        self.headers = None

        self.load_body_to_dict()
        try:
            logging.info(event)
            self.body = self.function(self.event, context)
            self.code = 200
        except HTTPException as ex:
            self.body = ex.body
            self.code = ex.code
            self.headers = ex.headers
        except Exception as ex:
            logging.exception(ex.message)
            self.body = HTTP_STATUS_CODES.get(500)
            self.code = 500

        return self.response()

    @property
    def content_type(self):
        return self.event.get('headers', {}).get('Content-Type')

    def load_body_to_dict(self):
        if self.content_type == 'application/json':
            self.event['body'] = json.loads(self.event.get('body') or '{}')
        if self.content_type == 'application/x-www-form-urlencoded':
            body = self.event.get('body') or ""
            self.event['body'] = urlparse.parse_qs(body, keep_blank_values=True)

    def response(self):
        result = {
            "statusCode": self.code,
            "body": self._body(),
            "headers": self._headers()
        }
        logging.info(result)
        return result

    def _body(self):
        if type(self.body) in [dict, list]:
            return json.dumps(self.body, sort_keys=True, indent=4, separators=(',', ': '))
        elif self.body is None:
            return {}
        else:
            return self.body

    def _headers(self):
        if self.headers is None:
            return {'Access-Control-Allow-Origin': "*"}
        else:
            return self.headers
