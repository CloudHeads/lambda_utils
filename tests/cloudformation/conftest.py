import json

import pytest


@pytest.fixture()
def stack_arn(region, account_id, stack_name):
    'arn:aws:cloudformation:{region}:{account_id}:stack/{stack_name}'.format(
        region=region,
        account_id=account_id,
        stack_name=stack_name
    )


@pytest.fixture()
def stack_id(stack_arn, unique_id):
    return "{stack_arn}/{unique_id}".format(stack_arn=stack_arn, unique_id=unique_id)


@pytest.fixture(params=['Create', 'Update', 'Delete'])
def request_type(request):
    return request.param


@pytest.fixture()
def logical_resource_id(random_string):
    return "LogicalResourceId{random_string}".format(random_string=random_string)


@pytest.fixture()
def custom_resource_event(request, region, account_id, stack_id, stack_name, request_type, lambda_arn, lambda_name, unique_id, logical_resource_id):
    return {
        'StackId': stack_id,
        'ResponseURL': 'https://cloudformation-custom-resource-response-euwest1.s3-eu-west-1.amazonaws.com/{stack_id}'.format(stack_id=stack_id),
        'RequestType': request_type,
        'ServiceToken': lambda_arn,
        'ResourceType': 'Custom::{lambda_name}'.format(lambda_name=lambda_name),
        'PhysicalResourceId': '{stack_name}-{logical_resource_id}'.format(stack_name=stack_name, logical_resource_id=logical_resource_id),
        'RequestId': unique_id,
        'LogicalResourceId': logical_resource_id,
        'ResourceProperties': {

        }

    }
