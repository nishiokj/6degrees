#!/bin/bash

# Define AWS profile, function name and AWS region
AWS_PROFILE="your_aws_profile"
FUNCTION_NAME="your_lambda_function_name"
AWS_REGION="your_aws_region"

# Make sure we are in the correct directory
cd /path/to/your/project/

# Remove the old zip file
rm dailyUpdate.zip

# Install dependencies
pip install -r requirements_aws.txt -t ./

# Zip the function code and its dependencies
zip -r dailyUpdate.zip .

# Update AWS Lambda with the new code
aws lambda update-function-code --function-name 6degreesDailyUpdates --zip-file fileb://dailyUpdate.zip

# Remove the installed dependencies
rm -r *
