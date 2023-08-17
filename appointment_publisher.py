from os import environ
from json import dumps
from boto3 import client
#TODO Make this code parallel instead of sequential
#from multiprocessing import Process, Pipe

#BOTO3 Clients
DYNAMODB_CLIENT = client('dynamodb')
SQS_CLIENT = client('sqs')

#Constants
DYNAMODB_TABLE = environ('DYNAMODB_TABLE')
SEPE_QUEUE = environ('SEPE_QUEUE')
SEG_SOCIAL_QUEUE = environ('SEG_SOCIAL_QUEUE')

def handler(_event, _context):
    user_list = DYNAMODB_CLIENT.scan(
        TableName=DYNAMODB_TABLE,
        IndexName='resource',
        FilterExpression='resource = :resource_name',
        ExpressionAttributeValues={':resource_name': 'user'}
    )

    appointment_list = DYNAMODB_CLIENT.scan(
        TableName=DYNAMODB_TABLE,
        IndexName='resource',
        FilterExpression='resource = :resource_name',
        ExpressionAttributeValues={':resource_name': 'appointment'}
    )

    for user in user_list['Items']:
        appointment_subscribed_list = user['appointment']
        for subscription in appointment_subscribed_list:
            for appointment in appointment_list['Items']:
                if subscription['N'] == appointment['id']:
                    match appointment['entity']:
                        case 'sepe':
                            print('Sepe entity')
                            send_queue_event(SEPE_QUEUE, user, appointment)
                            continue
   c
                        case _:
                            print('Unknown entity')
                            continue

def send_queue_event(queue_url, user, appointment):
    event = {"user": user, "appointment": appointment}
    response = SQS_CLIENT.send_message(
        QueueUrl=queue_url,
        MessageBody=dumps(event),
    )
