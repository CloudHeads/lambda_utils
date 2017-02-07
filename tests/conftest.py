import random
import string
import uuid

import pytest


@pytest.fixture()
def test_name(request):
    name = request.node.name
    for character in ['test_', '[', ']', '{', '}', '/']:
        name = name.replace(character, '')
    return name


@pytest.fixture()
def unique_id():
    return uuid.uuid4().hex


@pytest.fixture()
def random_string():
    valid_letters = string.ascii_letters + string.digits
    return ''.join((random.choice(valid_letters) for i in xrange(50)))


@pytest.fixture(params=['eu-west-1'])
def region(request):
    return request.param


@pytest.fixture()
def account_id():
    return [random.randint(0, 9) for p in range(0, 21)]


@pytest.fixture()
def stack_name(test_name, random_string):
    return 'stack-name-{test_name}-{random}'.format(stack_name=stack_name, test_name=test_name, random=random_string)


@pytest.fixture()
def lambda_name():
    return "LambdaFunctionName"


@pytest.fixture()
def lambda_arn(region, account_id, lambda_name):
    'arn:aws:lambda:{region}:{account_id}:{lambda_name}'.format(
        region=region,
        account_id=account_id,
        lambda_name=lambda_name
    )


@pytest.fixture
def context(test_name, unique_id, lambda_name):
    class LambdaContext(object):
        def __init__(self, version='LATEST'):
            self.version = version

        @property
        def get_remaining_time_in_millis(self):
            return 10000

        @property
        def function_name(self):
            return test_name

        @property
        def function_version(self):
            return self.version

        @property
        def invoked_function_arn(self):
            return 'arn:aws:lambda:serverless:' + lambda_name

        @property
        def memory_limit_in_mb(self):
            return 128

        @property
        def aws_request_id(self):
            return unique_id

    return LambdaContext()
