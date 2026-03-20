import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"

def lambda_handler(event, context):

    print("Received event:", json.dumps(event))

    if 'detail' not in event:
        print("Invalid event format")
        return

    instance_id = event['detail']['instance-id']
    state = event['detail']['state']
    region = event.get('region', 'unknown')

    message = f"""
EC2 Instance State Change Alert

Instance ID: {instance_id}
State: {state}
Region: {region}
"""

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="EC2 Instance State Change",
        Message=message
    )

    print("SNS notification sent")