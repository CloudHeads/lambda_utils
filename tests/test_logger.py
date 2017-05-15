import os
import logging
from time import sleep
from mock import patch
from lambda_utils.logger import Logger
from hamcrest import assert_that, equal_to
from tests.conftest import Context


class TestLogger:
    @patch.object(logging, 'debug')
    @patch.dict(os.environ, {'LOGLEVEL': 'DEBUG'})
    def test_configures_logger_to_debug_loglevel(self, debug_mock):
        @Logger()
        def function(event, context):
            return event

        function({'foo': 'bar'}, Context())

        assert_that(logging.getLogger().level, equal_to(logging.DEBUG))
        assert_that(debug_mock.call_count, equal_to(2))

    @patch.object(logging, 'debug')
    def test_configures_logger_with_defaults(self, debug_mock):
        @Logger()
        def function(event, context):
            pass

        function({'foo': 'bar'}, Context())

        assert_that(logging.getLogger().level, equal_to(logging.INFO))
        assert_that(debug_mock.call_count, equal_to(2))

    @patch.object(logging, 'error')
    def test_logs_error_on_timeout(self, error_mock):
        @Logger()
        def function(event, context):
            sleep(1)

        function(None, Context(600))

        assert_that(error_mock.call_count, equal_to(1))
        error_mock.assert_called_once_with('Execution is about to timeout.')

    @patch.object(logging, 'error')
    def test_logs_no_timeout_on_succeed(self, error_mock):
        @Logger()
        def function(event, context):
            pass

        function(None, Context(600))

        assert_that(error_mock.call_count, equal_to(0))
