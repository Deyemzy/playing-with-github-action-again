## playing-with-github-action-again

This GitHub Actions workflow performs code checks and deploys an S3 bucket and EC2 instance using AWS credentials and configuration details stored as secrets.

The workflow is triggered on any push to the main branch of the repository. It consists of two jobs: code-checks and deploy-s3-ec2.

The code-checks job runs on an Ubuntu latest environment and performs several code quality checks using tools such as Pylint, Flake8, and Bandit. It also downloads the configuration file from the S3 bucket and runs a security scan using Snyk. The job saves the Pylint score as an environment variable.

The deploy-s3-ec2 job runs if the push is to the main branch and deploys an S3 bucket and EC2 instance using the AWS SDK for Python (Boto3). It uses the same configuration file downloaded in the code-checks job to configure the AWS credentials and the EC2 instance details.

Finally, the code has been documented to aid in its understanding and maintenance in the future.

Signed: Lion 