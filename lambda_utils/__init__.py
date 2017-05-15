# -*- coding: utf-8 -*-
__author__ = """CloudHeads"""
__email__ = 'theguys@cloudheads.io'
__version__ = '0.2.0'

import json
import urlparse


def extract_body(event):
    def content_type():
        headers = event.get('headers', {})
        for key in ['Content-Type', 'content-type']:
            if key in headers:
                return headers[key]
        return ''

    body = None

    if 'application/json' in content_type():
        body = json.loads(event.get('body', '{}'))

    if 'application/x-www-form-urlencoded' in content_type():
        body = urlparse.parse_qs(event.get('body', ''), keep_blank_values=True)

    return body


def http_response(body, status=200, headers=None):
    default_headers = {'Access-Control-Allow-Origin': '*'}

    if headers:
        merged_headers = default_headers.copy()
        merged_headers.update(headers)
        headers = merged_headers
    else:
        headers = default_headers

    return {
        'statusCode': status,
        'body': body,
        'headers': headers
    }


def json_http_response(body, status=200, headers=None):
    json_body = json.dumps(body, sort_keys=True, indent=4, separators=(',', ': '))

    return http_response(json_body, status, headers)


def redirect_to(url, status=302):
    return http_response('', status=status, headers={'Location': url})

