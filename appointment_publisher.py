import os
import boto3
#TODO Make this code parallel instead of sequential
#from multiprocessing import Process, Pipe

#BOTO3 Clients
DYNAMODB_CLIENT = boto3.client('dynamodb')
SQS_CLIENT = boto3.client('sqs')

#Constants
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
SEPE_QUEUE = os.getenv('SEPE_QUEUE')

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
                            send_sepe_queue_event()
                            continue
                        case 'seg-social':
                            print('Seg-Social entity')
                            continue
                        case _:
                            print('Unknown entity')

def send_sepe_queue_event():
    response = SQS_CLIENT.send_message(
        QueueUrl=SEPE_QUEUE,
        MessageBody='string',
    )