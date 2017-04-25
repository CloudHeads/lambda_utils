from time import sleep

from pytest import fixture
import os
import logging
from mock import patch
from lambda_utils.logger import Logger
from hamcrest import assert_that, equal_to


class TestLogger:
    @patch.object(logging, 'debug')
    @patch.dict(os.environ, {'LOGLEVEL': 'DEBUG'})
    def test_configures_logger_to_debug_loglevel(self, debug_mock):
        @Logger()
        def function(event, context):
            return event

        function({'foo':'bar'}, None)

        assert_that(logging.getLogger().level, equal_to(logging.DEBUG))
        assert_that(debug_mock.call_count, equal_to(2))

    @patch.object(logging, 'debug')
    def test_configures_logger_with_defaults(self, debug_mock):
        @Logger()
        def function(event, context):
            pass

        function({'foo':'bar'}, None)

        assert_that(logging.getLogger().level, equal_to(logging.INFO))
        assert_that(debug_mock.call_count, equal_to(2))


