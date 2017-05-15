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
    'arn:aws:lambda:{region}:{account_id}:{lambda_name}'.format(region=region, account_id=account_id, lambda_name=lambda_name)


class Context:
    def __init__(self, milliseconds=None):
        self.milliseconds = milliseconds or 6000

    def get_remaining_time_in_millis(self):
        return self.milliseconds
