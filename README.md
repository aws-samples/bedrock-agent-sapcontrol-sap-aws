// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

## bedrock-agent-sapcontrol-sap-aws

Version 1.0

Authors: Gergely Cserdi (AWS), Harsh Thoria (AWS), Otavio Nunes (AWS)

Purpose:
This repo is related to the SAP on AWS Blog: << BLOG LINK HERE >>

It contains Python code for AWS Lambda and other json files that help facilitate the creation of
Bedrock agent and SAPControl service solution that is demo'ed in the blog

In the blog, a demo solution is presented how to use Amazon Bedrock Agents powered by LLM to carry out standard SAP 
operational tasks. The solution is mapping an AWS Lambda function to the Amazon Bedrock Agent and uses a webproxy solution, called zeep to interact with SAPcontrol process on the SAP instance host.

Files:
README.md                       - This file that you're reading that explains the purpose of the repo
SAPControlBedrockAgentLambda.py - Sample code in Python that should be added to the AWS Lambda function
SAPControlLambdaSSMParam.json   - Sample inline permission policy that allows Lambda function to look up SSM parameters
get-parameter-value.json        - Sample JSON for the Amazon Bedrock Agent parameter value lookup feature
get-process-status.json         - Sample JSON for the Amazon Bedrock Agent SAP system status check feature
load-logfiles-to-s3.json        - Sample JSON for the Amazon Bedrock Agent SAP log upload to S3 bucket feature
startinstance.json              - Sample JSON for the Amazon Bedrock Agent SAP instance start feature
stopinstance.json               - Sample JSON for the Amazon Bedrock Agent SAP instance stop feature
requirements.txt                - Python pacakge requirements to build the AWS Lambda layer

Please note that you may use different combinations of Python packages that best fit your needs. In that case feel free to update the requirements.txt file.


## License

This library is licensed under the MIT-0 License. See the LICENSE file.

