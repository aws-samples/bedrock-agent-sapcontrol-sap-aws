# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    # Getting inbound parameters
    param_dict = {param['name'].lower(): param['value'] for param in parameters}

    # Parsing general inbound parameters 
    sapsid = param_dict.get('sapsid')
    saphostnameip = param_dict.get('hostnameip')

    # Parsing function specific inbound parameters 
    if function == "get-parameter-value":
        sapparameter = param_dict.get('parametername')

    if function == "load-logfiles-to-s3":
        s3bucketname = param_dict.get('s3bucketname')

    
    # Get password stored in secure store
    ssmclient = boto3.client('ssm', region_name='us-east-1')    

    sidadmuser = sapsid.lower() + 'adm'
    ssmparamresult = ssmclient.get_parameter(Name=sidadmuser, WithDecryption=True)
    sidadmpwd = ssmparamresult['Parameter']['Value']
    
    sapsidno = sapsid.lower() + 'no'
    ssmparamresult = ssmclient.get_parameter(Name=sapsidno, WithDecryption=False)
    sidno = ssmparamresult['Parameter']['Value']

    ssid = sapsid.upper()

    # Initiating the WebProxy session to SAPHOSTCONTROL
    session = Session()
    session.auth = HTTPBasicAuth(sidadmuser, sidadmpwd)
    url = 'http://' + str(saphostnameip) + ':5' + str(sidno) + '13?wsdl'
    zeep_client = Client(url,transport=Transport(session=session))
    
    # Based on what exactly the function is we execute the correct SOAP call
    if function == "get-parameter-value":
        result = zeep_client.service.ParameterValue(sapparameter)
        result_text = "The parameter has a value of {} ".format(result)
    
    if function == "load-logfiles-to-s3":
        aws3command = f'/usr/local/bin/aws s3 cp /usr/sap/{ssid}/D{sidno}/work/ {s3bucketname} --recursive'
        result = zeep_client.service.OSExecute(aws3command, 0, 3600)
        result_text = "Log files uploaded to S3 bucket"
        
    if function == "stopinstance":
        result = zeep_client.service.Stop()
        result_text = "SAP system {} stop initiated.".format(sapsid)
        
    if function == "startinstance": 
        result = zeep_client.service.Start()
        result_text = "SAP system {} start initiated.".format(sapsid)
        
    if function == "get-process-status":
        result = zeep_client.service.GetProcessList()
        result_text = "Process Status {}".format(result)       
        

    response_body = {
        "TEXT": {
            "body": result_text
        }
    }
    
    function_response = {
        'actionGroup': event['actionGroup'],
        'function': event['function'],
        'functionResponse': {
            'responseBody': response_body
        }
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    action_response = {
        'messageVersion': '1.0', 
        'response': function_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return action_response


