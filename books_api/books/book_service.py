from boto3 import resource
from django.conf import settings

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
REGION_NAME = settings.REGION_NAME
ENDPOINT_URL = settings.ENDPOINT_URL

resource = resource(
    'dynamodb',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


def create_table_book():
    table = resource.create_table(
        TableName='Book',  # Name of the table
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # HASH = partition key, RANGE = sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',  # Name of the attribute
                'AttributeType': 'N'  # N = Number (S = String, B= Binary)
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


BookTable = resource.Table('Book')


def write_to_book(id, title, description, author, publisher, year, isbn):
    response = BookTable.put_item(
        Item={
            'id': id,
            'title': title,
            'description': description,
            'author': author,
            'publisher': publisher,
            'year': year,
            'isbn': isbn,
            'upvotes': 0
        }
    )
    return response


def read_from_book(id):
    response = BookTable.get_item(
        Key={
            'id': id
        },
        AttributesToGet=['title', 'description', 'author', 'publisher', 'year', 'isbn', 'upvotes']
    )
    return response


def update_in_book(id, data: dict):
    response = BookTable.update_item(
        Key={
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value': data['title'],
                'Action': 'PUT'  # # available options = DELETE(delete), PUT(set/update), ADD(increment)
            },
            'description': {
                'Value': data['description'],
                'Action': 'PUT'
            },
            'author': {
                'Value': data['author'],
                'Action': 'PUT'
            },
            'publisher': {
                'Value': data['publisher'],
                'Action': 'PUT'
            },
            'year': {
                'Value': data['year'],
                'Action': 'PUT'
            },
            'isbn': {
                'Value': data['isbn'],
                'Action': 'PUT'
            }
        },
        ReturnValues="UPDATED_NEW"  # returns the new updated values
    )
    return response


def upvote_a_book(id):
    response = BookTable.update_item(
        Key={
            'id': id
        },
        AttributeUpdates={
            'upvotes': {
                'Value': 1,
                'Action': 'ADD'
            }
        },
        ReturnValues="UPDATED_NEW"
    )
    response['Attributes']['upvotes'] = int(response['Attributes']['upvotes'])
    return response


def delete_from_book(id):
    response = BookTable.delete_item(
        Key={
            'id': id
        }
    )

    return response
