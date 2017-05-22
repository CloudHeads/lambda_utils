import pytest
from hamcrest import assert_that, equal_to
from pytest import fixture
from mock import patch

from lambda_utils import LambdaProcessor
from lambda_utils.response_handlers import cloudformation as module
from lambda_utils.response_handlers.cloudformation import Cloudformation, FAILED, send_signal


@fixture
def event():
    return {
        'StackId': 'stack_id',
        'ResponseURL': 'https://cloudformation-custom-resource-response-euwest1.s3-eu-west-1.amazonaws.com/stack_id',
        'RequestType': 'CREATE',
        'ServiceToken': "some_lambda_arn",
        'ResourceType': 'Custom::CustomResource',
        'PhysicalResourceId': 'stack_name-logical_resource_id',
        'RequestId': 'request_id',
        'LogicalResourceId': 'logical_resource_id',
        'ResourceProperties': {}
    }


class TestCloudformation:
    def test_on_execution_store_event(self, event):
        cloudformation = Cloudformation()

        result = cloudformation.on_execution(event)

        assert_that(result, equal_to(event))
        assert_that(cloudformation.event, equal_to(event))

    @patch.object(module, 'send_signal')
    def test_on_exception_failed_signal_is_send(self, send_signal_mock, event):
        exception = Exception('some_exception')

        @LambdaProcessor(response_handler=Cloudformation)
        def function(event, context):
            raise exception

        with pytest.raises(Exception) as ex:
            function(event, None)

        assert_that(ex.value, equal_to(exception))
        send_signal_mock.assert_called_once_with(event, FAILED, exception.message)


class TestSendSignal:
    @patch.object(module.urllib2, 'build_opener')
    def test_send_signal(self, build_opener, event):
        send_signal(event, 'SUCCESS', 'some_random_string')

        build_opener.assert_called_once_with(module.urllib2.HTTPHandler)
        build_opener.return_value.open.assert_called_once()

    @patch.object(module.urllib2, 'build_opener')
    def test_send_signal_non_serializable_reason(self, build_opener, event):
        send_signal(event, 'SUCCESS', object())

        build_opener.assert_called_once_with(module.urllib2.HTTPHandler)
        build_opener.return_value.open.assert_called_once()
