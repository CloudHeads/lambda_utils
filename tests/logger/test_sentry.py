import logging
import os
import uuid

from hamcrest import assert_that, equal_to
from mock import patch
from pytest import fixture

from lambda_utils.logger import sentry as module
from lambda_utils.logger.sentry import Sentry


@fixture
def x_amzn_trace_id():
    return "Root:%s" % uuid.uuid4()


@fixture
def event(x_amzn_trace_id):
    return {'requestContext': {"authorizer": {"Key": "value"}}, 'headers': {'X-Amzn-Trace-Id': x_amzn_trace_id}}


class TestSentry:
    @patch.dict(os.environ, {'SENTRY_IO': 'https://some:dsn@app.getsentry.com/123', 'AWS_LAMBDA_FUNCTION_NAME': "some_name"})
    def test_on_call_initialize_sentry_as_logger(self):
        sentry = Sentry()
        sentry.on_init(lambda x: x)

        assert_that(len(logging.getLogger('raven').handlers), equal_to(1))
        assert_that(sentry.client.name, equal_to('some_name'))
        assert_that(sentry.handler.client, equal_to(sentry.client))
        assert_that(sentry.handler.level, equal_to(logging.ERROR))

    @patch.object(module.Sentry, 'add_x_ray_tags')
    @patch.object(module.Sentry, 'add_user_context')
    def test_on_execution(self, x_ray_mock, user_context_mock, event):
        Sentry().on_execution(event)

        x_ray_mock.assert_called_once_with(event)
        user_context_mock.assert_called_once_with(event)

    @patch.object(module.Sentry, 'client')
    def test_add_user_context_set_client_context(self, client_mock, event):
        Sentry().add_user_context(event)

        client_mock.user_context.assert_called_once_with({'key': 'value'})

    @patch.object(logging, 'debug')
    def test_add_user_context_with_none_event(self, debug_mock, event):
        Sentry().add_user_context(None)

        debug_mock.assert_called_once()

    @patch.object(module.Sentry, 'client')
    def test_add_x_ray_tags_adds_requester_trace_id(self, client_mock, event, x_amzn_trace_id):
        Sentry().add_x_ray_tags(event)

        client_mock.tags_context.assert_called_once_with({'Request-X-Amzn-Trace-Id': x_amzn_trace_id})

    @patch.dict(os.environ, {'_X_AMZN_TRACE_ID': 'some_id'})
    @patch.object(module.Sentry, 'client')
    def test_add_x_ray_tags_adds_lambda_trace_id(self, client_mock):
        Sentry().add_x_ray_tags({})

        client_mock.tags_context.assert_called_once_with({'X-Amzn-Trace-Id': 'some_id'})

    @patch.dict(os.environ, {'_X_AMZN_TRACE_ID': 'some_id'})
    @patch.object(module.Sentry, 'client')
    def test_add_x_ray_tags_with_none_event(self, client_mock):
        Sentry().add_x_ray_tags(None)

        client_mock.tags_context.assert_called_once_with({'X-Amzn-Trace-Id': 'some_id'})
