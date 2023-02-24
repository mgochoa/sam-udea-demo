# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
from datetime import datetime
import time

TABLE_NAME = 'VisitorData'
dynamodb_client = boto3.client('dynamodb')
table = dynamodb_client.Table(TABLE_NAME)


def get_unix_time():
    """Returns current unix timestamp"""
    d = datetime.utcnow()
    return time.mktime(d.timetuple())


def add_visit(user_agent):
    visit_id = get_unix_time()
    item = {
        'id': visit_id,
        'user_agent': user_agent
    }
    dynamodb_client.put_item(TableName=TABLE_NAME, Item=item)


def get_total_count():
    return table.scan()['Count']


def lambda_handler(event, context):
    add_visit(context['identity'].get('userAgent'))
    total_count = get_total_count()
    return {
        'statusCode': 200,
        'body': f'Visited {total_count} times'
    }
