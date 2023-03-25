"""
Playing with github action again

Author: Lion Adigun
Date: 2023-03-25
"""

import sys
import configparser
import boto3

# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Create S3 bucket if it doesn't exist
s3_client = boto3.client(
    's3',
    aws_access_key_id=config['aws']['access_key_id'],
    aws_secret_access_key=config['aws']['secret_access_key'],
    region_name=config['aws']['region']
)
bucket_name = config['s3']['bucket_name']
lb = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]
if bucket_name not in lb:
    s3_client.create_bucket(Bucket=bucket_name)

# Check if EC2 instance already exists
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=config['aws']['access_key_id'],
    aws_secret_access_key=config['aws']['secret_access_key'],
    region_name=config['aws']['region']
)
instance_name = config['ec2']['instance_name']
instance_filter = [{'Name': 'tag:Name', 'Values': [instance_name]}]
existing_instances = ec2_client.describe_instances(Filters=instance_filter)
if len(existing_instances['Reservations']) > 0:
    instance_id = existing_instances[
        'Reservations'][0]['Instances'][0]['InstanceId']
    instance = ec2_client.describe_instances(
        InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    print(f"Using existing EC2 instance with ID {instance_id}")
else:
    # Create new EC2 instance if it doesn't exist
    key_pair_name = config['ec2']['key_pair_name']
    try:
        key_pair = ec2_client.describe_key_pairs(
            KeyNames=[key_pair_name]
            )['KeyPairs'][0]
    except ec2_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
            print(f'Error: Key pair {key_pair_name} not found.')
            sys.exit(1)
        else:
            raise
    instance_type = config['ec2']['instance_type']
    ami_id = config['ec2']['ami_id']
    security_groups = ec2_client.describe_security_groups(
        Filters=[{'Name': 'group-name', 'Values': ['default']}]
    )['SecurityGroups']
    security_group_id = security_groups[0]['GroupId']
    instance = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_pair_name,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': instance_name}]
        }]
    )['Instances'][0]
    instance_id = instance['InstanceId']
    print(f"Created new EC2 instance with ID {instance_id}")

# Tag the instance
ec2_client.create_tags(
    Resources=[instance_id], Tags=[{'Key': 'Name', 'Value': instance_name}])

