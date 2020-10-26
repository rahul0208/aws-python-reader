import json
import os

import boto3
import pytest
from moto import mock_config, mock_s3, mock_iam

from aws_servicer import aws_client


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture()
@mock_s3
def s3(aws_credentials):
    client = boto3.resource('s3')
    client.create_bucket(Bucket=f'mock-bucket')

@pytest.fixture()
@mock_s3
def s3_100(aws_credentials):
    client = boto3.resource('s3')
    for i in range(110):
        client.create_bucket(Bucket=f'mock-bucket-{i}')



@pytest.fixture()
@mock_iam
def iam(aws_credentials):
    client = boto3.client('iam')
    policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "ec2:Describe*",
                "Resource": "*"
            }
        ]
    })
    instance = client.create_policy(PolicyName='mock-policy', PolicyDocument=policy_document)
    print(instance)

    role = client.create_role(RoleName='mock-role', AssumeRolePolicyDocument=policy_document)
    print(role)


@pytest.fixture()
def mock_aws_infra(s3, iam):
    yield

@mock_config
def test_should_find_resources_of_different_types(mock_aws_infra):
    resources = aws_client.read_all_resources()
    assert resources
    assert len(resources) == 3

@mock_config
def test_should_find_all_paginated_resources(s3_100):
    resources = aws_client.read_all_resources()
    assert resources
    assert len(resources) == 110
