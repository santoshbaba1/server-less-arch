import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Get latest AMI
    images = ec2.describe_images(Owners=['self'])['Images']

    latest_image = sorted(
        images,
        key=lambda x: x['CreationDate'],
        reverse=True
    )[0]

    image_id = latest_image['ImageId']

    print(f"Latest AMI: {image_id}")

    # Launch instance
    instance = ec2.run_instances(
    ImageId='ami-0d9ee65a2a86e323b',
    InstanceType='t4g.micro',
    MinCount=1,
    MaxCount=1,

    # ✅ REQUIRED FIX
    NetworkInterfaces=[
        {
            'SubnetId': 'subnet-05fd5e23acdd5b9e8',
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': ['sg-0328dc2b2e1069b9b']
        }
        ]
    )

    instance_id = instance['Instances'][0]['InstanceId']

    print(f"Instance created: {instance_id}")