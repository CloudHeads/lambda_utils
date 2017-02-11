import json

import pytest

from lambda_utils.api_gateway import ApiGateway
from lambda_utils.exceptions import *


@ApiGateway()
def function(event, context):
    return event


def test_successful_response(event, context):
    result = function(event, context)

    assert result['statusCode'] == 200
    assert json.loads(result['body']) == event


def test_access_control_allow_origion_header_is_set(event, context):
    result = function(event, context)

    assert result['headers']['Access-Control-Allow-Origin'] == "*"


@pytest.mark.parametrize('exception', [
    BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, NotAcceptable, RequestTimeout, Conflict, Gone, LengthRequired, PreconditionFailed,
    RequestEntityTooLarge, RequestURITooLarge, UnsupportedMediaType, RequestedRangeNotSatisfiable, ExpectationFailed, UnprocessableEntity,
    PreconditionRequired, TooManyRequests, RequestHeaderFieldsTooLarge, InternalServerError, BadGateway, ServiceUnavailable, HTTPVersionNotSupported
])
def test_http_exception(event, context, exception):
    @ApiGateway()
    def function(event, context):
        raise exception()

    result = function(event, context)

    assert result['statusCode'] == exception.code
    assert result['body'] == HTTP_STATUS_CODES.get(exception.code)
