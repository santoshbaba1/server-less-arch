import boto3

def lambda_handler(event, context):
    elbv2 = boto3.client('elbv2')
    sns = boto3.client('sns')
    
    TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:ap-south-1:251478238405:targetgroup/elb-sns-tgt/3470af8b7d587097"
    SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:251478238405:elb-health-alerts"
    
    response = elbv2.describe_target_health(
        TargetGroupArn=TARGET_GROUP_ARN
    )
    
    unhealthy_instances = []
    
    for target in response['TargetHealthDescriptions']:
        instance_id = target['Target']['Id']
        state = target['TargetHealth']['State']
        
        if state != 'healthy':
            unhealthy_instances.append({
                "InstanceId": instance_id,
                "State": state
            })
    
    if unhealthy_instances:
        message = "🚨 Unhealthy Instances Detected:\n"
        
        for inst in unhealthy_instances:
            message += f"Instance: {inst['InstanceId']} | State: {inst['State']}\n"
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="ALB Health Alert",
            Message=message
        )
        
        print(message)
    else:
        print("✅ All instances are healthy")
    
    return {
        'statusCode': 200,
        'body': unhealthy_instances
    }