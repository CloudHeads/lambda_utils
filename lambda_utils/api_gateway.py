from lambda_utils import Event


class Cloudformation(Event):
    event = None
    status = None
    response = None
    reason = None

    def wrapped_function(self, event, context):
        self.event = dict(event)
        if self.if_sns_event:
            self.event = json.loads(event['Records'][0]['Sns']['Message'])
        self.status = 'FAILED'
        self.response = None
        self.reason = context.aws_request_id

        try:
            self.response = self.function(self.event, context)
            self.status = 'SUCCESS'
            return self.response
        except Exception as ex:
            self.reason = ex.message
            raise
        finally:
            send_signal(self.event, self.status, self.reason, self.response)
