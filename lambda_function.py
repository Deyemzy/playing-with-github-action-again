"""
Playing with github action again

Author: Lion Adigun
Date: 2023-03-25
"""

import configparser
import boto3

# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Create S3 bucket
s3_client = boto3.client(
    's3',
    aws_access_key_id=config['aws']['access_key_id'],
    aws_secret_access_key=config['aws']['secret_access_key'],
    region_name=config['aws']['region']
)
bucket_name = config['s3']['bucket_name']
s3_client.create_bucket(Bucket=bucket_name)

# Create EC2 instance
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=config['aws']['access_key_id'],
    aws_secret_access_key=config['aws']['secret_access_key'],
    region_name=config['aws']['region']
)
key_pair_name = config['ec2']['key_pair_name']
instance_type = config['ec2']['instance_type']
ami_id = config['ec2']['ami_id']
key_pair = ec2_client.create_key_pair(KeyName=key_pair_name)
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
    SecurityGroupIds=[security_group_id]
)['Instances'][0]
