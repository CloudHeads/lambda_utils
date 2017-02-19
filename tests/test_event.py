import os
import logging
import pytest

from lambda_utils import Event


@pytest.mark.parametrize('debug,log_level', [(None, logging.INFO), ('false', logging.ERROR), ('true', logging.INFO)])
def test_debug_environment(debug, log_level, context):
    if debug:
        os.environ['DEBUG'] = debug
    else:
        os.environ.pop('DEBUG', None)

    @Event()
    def function(event, context):
        return event

    function({}, context)
    assert logging.getLogger().level == log_level


def test_sentry_io_handler(context):
    os.environ['SENTRY_IO'] = 'https://key:key@app.getsentry.com/12345'

    @Event()
    def function(event, context):
        return event

    function({}, context)
    assert len(logging.getLogger('raven').handlers) == 1
