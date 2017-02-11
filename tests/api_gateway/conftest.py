import pytest


@pytest.fixture
def event():
    return {
        "body": {},
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "de,en-US;q=0.8,en;q=0.6",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "DE",
            "Content-Type": 'application/json',
            "DNT": "1",
            "Origin": "https://localhost",
            "Host": "some.execute-api.eu-west-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
            "Via": "1.1 some.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "C4wnLw2jWf3MYKSKK4Q4VfIa2Iv2gPndyQ5IAzlMc881sWUoUEns0Q==",
            "X-Forwarded-For": "8.8.8.8, 4.4.4.4",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "httpMethod": "GET",
        "isBase64Encoded": False,
        "path": "/",
        "pathParameters": None,
        "queryStringParameters": None,
        "requestContext": {
            "accountId": "some_account_id|",
            "apiId": "some_api_id",
            "httpMethod": "GET",
            "identity": {
                "accessKey": None,
                "accountId": None,
                "apiKey": None,
                "caller": None,
                "cognitoAuthenticationProvider": None,
                "cognitoAuthenticationType": None,
                "cognitoIdentityId": None,
                "cognitoIdentityPoolId": None,
                "sourceIp": "8.8.8.8",
                "user": None,
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
                "userArn": None
            },
            "requestId": "c5a26406-c76f-11e6-8ede-83f4755e886d",
            "resourceId": "12345678abc",
            "resourcePath": "/",
            "authorizer": None,
            "stage": 'development'
        },
        "resource": "/",
        "stageVariables": None
    }
