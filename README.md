# Serverless Architecture
# ✅ Assignment 17:

    Restore EC2 Instance from Snapshot
    This is a classic disaster recovery automation used in DevOps.
        use:
            Amazon EC2
            AWS Lambda
            Amazon EventBridge
            Boto3

# Objective
    Automatically:

        Find latest snapshot
                ↓
        Create volume
                ↓
        Launch new EC2 instance

# Architecture
        EBS Snapshots
              │
              ▼
        Lambda Function
              │
              ▼
        New EC2 Instance Created
              │
              ▼
        (Optional) EventBridge Trigger

# Deployment
## Prerequisite
    Must have:
    ✔ Existing EC2 instance
    ✔ Snapshots created 
    Check:
        EC2 → Elastic Block Store → Snapshots

# Create IAM Role for Lambda
    Go to:
    IAM → Roles → Create Role
        Attach policies:
        AmazonEC2FullAccess
    Role:
        Name: Lambda-EC2-Restore-Role
<img width="1318" height="675" alt="as17-iam role" src="https://github.com/user-attachments/assets/c67f4bf3-eb71-4842-9ee1-5b9b70adfdbb" />

# Create Lambda Function
    Go to:
    Lambda → Create Function
    Settings:
    Field	        Value
    Name	        EC2-Restore-From-Snapshot
    Runtime	        Python 3.x
    Role	        Lambda-EC2-Restore-Role
<img width="1316" height="659" alt="as17-lambda-funj" src="https://github.com/user-attachments/assets/ab6a6cd0-02d4-449c-89a9-789015042168" />

# Lambda Code (Core Logic)
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
            
                #  REQUIRED FIX
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

# Testing
    Manual Test
        Click:
        Lambda → Test
<img width="1310" height="669" alt="as17-ec2-restore" src="https://github.com/user-attachments/assets/0b178519-b4b6-4098-95fc-650b89a53d65" />
<img width="1310" height="669" alt="as17-ec2-restore-1" src="https://github.com/user-attachments/assets/6e67f72c-136b-45c5-80b0-ece7beb2a2cc" />

# Logs:

    Latest snapshot: snap-12345
    New EC2 instance launched: i-12345
<img width="1316" height="667" alt="as17-launch-ec2-inst" src="https://github.com/user-attachments/assets/fcd7db9f-17e0-4984-a733-6bd7b4cefed5" />

<img width="1314" height="663" alt="as17-log" src="https://github.com/user-attachments/assets/9e188509-99dc-4340-9a63-033640bb75c7" />

# Real Use Cases
    Disaster recovery
    Backup restore
    Auto failover
    Testing environments

# Final Flow
    Snapshot → EC2 Instance

# Key Learnings
    Snapshot vs AMI difference
    Lambda automation
    EC2 provisioning via Boto3
    Disaster recovery design

👨‍💻 Author

Santosh Kumar Sharma (12394), Batch-15

DevOps & Cloud Enthusiast

