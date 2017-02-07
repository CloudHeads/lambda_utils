import pytest
from mock import patch

from lambda_utils import cloudformation as module
from lambda_utils.cloudformation import Cloudformation, send_signal


@patch.object(module, 'send_signal')
def test_function_response(send_signal_mock, custom_resource_event, context):
    @Cloudformation()
    def function(event, context):
        return event

    function(custom_resource_event, context)

    send_signal_mock.assert_called_once_with(custom_resource_event, 'SUCCESS', None, custom_resource_event)


@patch.object(module, 'send_signal')
def test_exception_raised(send_signal_mock, custom_resource_event, context, random_string):
    @Cloudformation()
    def function(event, context):
        raise Exception(random_string)

    with pytest.raises(Exception):
        function(custom_resource_event, context)

    send_signal_mock.assert_called_once_with(custom_resource_event, 'FAILED', random_string, None)


@patch.object(module.urllib2, 'build_opener')
def test_send_signal(build_opener, custom_resource_event, random_string):
    send_signal(custom_resource_event, 'SUCCESS', random_string)

    build_opener.assert_called_once_with(module.urllib2.HTTPHandler)
    build_opener.return_value.open.assert_called_once()
