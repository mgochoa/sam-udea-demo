import boto3
from datetime import datetime
import time

TABLE_NAME = 'VisitorData'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def get_unix_time():
    """Returns current unix timestamp"""
    d = datetime.utcnow()
    return str(time.mktime(d.timetuple()))


def add_visit(user_agent):
    visit_id = get_unix_time()
    item = {
        'id': visit_id,
        'user_agent': user_agent
    }
    table.put_item(Item=item)


def get_total_count():
    return table.scan()['Count']


def lambda_handler(event, context):
    add_visit(event['requestContext']['identity'].get('userAgent'))
    total_count = get_total_count()
    return {
        'statusCode': 200,
        'headers': {
            'content-type': 'text/html'
        },
        'body': f'<h1>Visited {total_count} times</h1>'
    }
