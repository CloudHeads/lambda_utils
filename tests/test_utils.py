from lambda_utils import extract_body, http_response, json_http_response, redirect_to
from hamcrest import assert_that, equal_to, has_entry


class TestExtractBody:
    def test_returns_none_for_missing_content_headers(self):
        result = extract_body({})

        assert_that(result, equal_to(None))

    def test_recognizes_content_type_header_in_lower_case(self):
        result = extract_body({'headers': {'content-type': 'application/json'},
                               'body': '{"foo":"bar"}'})

        assert_that(result, equal_to({'foo': 'bar'}))

    def test_recognizes_content_type_header_in_upper_case(self):
        result = extract_body({'headers': {'Content-Type': 'application/json'},
                               'body': '{"foo":"bar"}'})

        assert_that(result, equal_to({'foo': 'bar'}))

    def test_returns_empty_dict_for_missing_body_with_json(self):
        result = extract_body({'headers': {'Content-Type': 'application/json'}})

        assert_that(result, equal_to({}))

    def test_returns_empty_dict_for_missing_body_with_x_www_form_urlencoded(self):
        result = extract_body({'headers': {'Content-Type': 'application/x-www-form-urlencoded'}})

        assert_that(result, equal_to({}))

    def test_returns_dict_for_valid_json_body(self):
        result = extract_body({'headers': {'Content-Type': 'application/json'},
                               'body': '{"foo":"bar"}'})

        assert_that(result, equal_to({'foo': 'bar'}))

    def test_returns_dict_for_valid_x_www_form_urlencoded_body(self):
        result = extract_body({'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
                               'body':'string=a&empty&special=%21%40J%23%3ALOIJ'})

        assert_that(result['string'], equal_to(['a']))
        assert_that(result['empty'], equal_to(['']))
        assert_that(result['special'], equal_to(['!@J#:LOIJ']))


class TestHttpResponse:
    def test_returns_200_http_status_code_as_default(self):
        result = http_response('Foo')

        assert_that(result['statusCode'], equal_to(200))

    def test_returns_string_as_default_body(self):
        result = http_response('Foo')

        assert_that(result['body'], equal_to('Foo'))

    def test_returns_default_headers(self):
        result = http_response('Foo')

        assert_that(result['headers'], has_entry('Access-Control-Allow-Origin', '*'))

    def test_merges_additional_headers_with_default_headers(self):
        result = http_response('Foo', headers={'Cache-Control': 'no-cache'})

        assert_that(result['headers'], has_entry('Access-Control-Allow-Origin', '*'))
        assert_that(result['headers'], has_entry('Cache-Control', 'no-cache'))
        assert_that(len(result['headers']), equal_to(2))

    def test_allows_to_overwrite_default_headers(self):
        result = http_response('Foo', headers={'Access-Control-Allow-Origin': 'https://my-prtg.com'})

        assert_that(result['headers'], has_entry('Access-Control-Allow-Origin', 'https://my-prtg.com'))
        assert_that(len(result['headers']), equal_to(1))


class TestJsonHttpResponse:
    def test_encodes_dict_body_as_valid_json(self):
        result = json_http_response({'foo': 'bar'})

        assert_that(result, has_entry('body', '{\n    "foo": "bar"\n}'))

    def test_passes_status_argument_on_to_http_response(self):
        result = json_http_response({'foo': 'bar'}, status=404)

        assert_that(result, has_entry('statusCode', 404))

    def test_passes_headers_argument_on_to_http_response(self):
        result = json_http_response({'foo': 'bar'}, headers={'Cache-Control': 'no-cache'})

        assert_that(result, has_entry('headers', {'Access-Control-Allow-Origin': '*', 'Cache-Control': 'no-cache'}))


class TestRedirectTo:
    def test_redirect_to_with_defaults(self):
        result = redirect_to('http://foo.com')

        assert_that(result['statusCode'], equal_to(302))
        assert_that(result, has_entry('headers', {'Access-Control-Allow-Origin': '*', 'Location': 'http://foo.com'}))

    def test_redirect_to_with_a_custom_status(self):
        result = redirect_to('http://foo.com', status=301)

        assert_that(result['statusCode'], equal_to(301))
        assert_that(result, has_entry('headers', {'Access-Control-Allow-Origin': '*', 'Location': 'http://foo.com'}))

