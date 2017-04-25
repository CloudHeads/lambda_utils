import os
import logging
from lambda_utils.sentry_expception_logger import SentryExceptionLogger
from hamcrest import assert_that, equal_to
from mock import patch


class TestSentryExceptionLogger:
    @patch.dict(os.environ, {'SENTRY_IO': 'https://key:key@app.getsentry.com/12345'})
    def test_configures_logger(self):

        @SentryExceptionLogger()
        def function(event, context):
            return event

        function({'foo': 'bar'}, None)
        assert_that(len(logging.getLogger('raven').handlers), equal_to(1))

