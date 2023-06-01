import boto3

client = boto3.resource('sqs',
                        endpoint_url='http://localhost:9324',
                        region_name='elasticmq',
                        aws_secret_access_key='x',
                        aws_access_key_id='x',
                        use_ssl=False)
queue = client.get_queue_by_name(QueueName='test')
while True:
    messages = queue.receive_messages(WaitTimeSeconds=10)
    if len(messages) != 0:
        print(messages[0].body)
        queue.delete_messages(Entries=[{'Id': 'randomstring', 'ReceiptHandle': messages[0].receipt_handle}])
