import json
import boto3
import os
import logging
from template import generate_code_template

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a Bedrock Runtime client
bedrock_client = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    logger.info('Event: %s', json.dumps(event))

    try:
        # API Gateway with Lambda Proxy Integration usually sends body as a string
        if isinstance(event.get('body'), str):
            request_body = json.loads(event['body'])
        else:
            request_body = event.get('body', {})
            
        # Extract the user's prompt from the frontend
        user_content = request_body.get('content', '')
        
        # Format the prompt using standard Python
        prompt = generate_code_template(context=user_content)
        
        # Create the message array required by the Converse API
        messages = [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
        
        # Define the inference configuration
        # Amazon Nova accepts maxTokens, temperature, and topP here
        inference_config = {
            "maxTokens": 1000,
            "temperature": 0.1,
            "topP": 0.2
        }
        
        # Use the environment variable, defaulting to the cross-region profile for Nova Micro
        model_id = os.environ.get('BEDROCK_MODEL_ID', 'us.amazon.nova-micro-v1:0')
        
        # Call the Converse API (without additionalModelRequestFields)
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config
        )

        logger.info('Response payload: %s', json.dumps(response))
        
        # Extract the generated text from the Converse response
        generated_text = ""
        for content_item in response['output']['message']['content']:
            if "text" in content_item:
                generated_text += content_item["text"]
        
        # Return the successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': generated_text
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }