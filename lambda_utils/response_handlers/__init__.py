class BaseResponseHandler:
    def on_execution(self, event):
        return event

    def on_exception(self, ex):
        raise

    def on_response(self, response):
        return response
