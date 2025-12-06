import boto3
import botocore.config
import json
from datetime import datetime

def generate_code_using_bedrock(message: str, language: str) -> str:
    prompt = f"""Write {language} code for the following instruction - 

    {message}

    Output ONLY raw {language} code.
    Do NOT include explanation, comment, markdown, backtick, or text of any kind.
    Return ONLY the final code."""


    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1", config=botocore.config.Config(read_timeout=300, retries = {'max_attempts': 3}))
        response = bedrock.invoke_model(
            body=json.dumps(body),
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
        )
        response_content = response.get("body").read().decode("utf-8")
        response_json = json.loads(response_content)
        code = response_json["content"][0]["text"].strip()
        return code
    except Exception as e:
        print("Error generating code - ", e)
        return ""

def save_code_to_s3_bucket(code, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=code)
        print("Code saved to S3 bucket successfully.")
    except Exception as e:
        print("Error saving code to S3 bucket - ", e)

def generate_pre_signed_url(s3_bucket, s3_key):
    s3 = boto3.client('s3')
    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': s3_bucket, 'Key': s3_key},
        ExpiresIn=3600
    )
    return presigned_url


def lambda_handler(event, context):
    event = json.loads(event['body'])
    message = event['message']
    language = event['key']
    print("Message - ", message)
    print("Language - ", language)
    generated_code = generate_code_using_bedrock(message, language)
    download_url = ""
    if generated_code:
        current_time = datetime.now().strftime("%H:%M:%S")
        s3_key = f'code-output/{current_time}.py'
        s3_bucket = 'bedrock-bucket-hr'
        save_code_to_s3_bucket(generated_code, s3_bucket, s3_key)
        download_url = generate_pre_signed_url(s3_bucket, s3_key)
    else:
        print("Failed to generate code.")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Code generation complete.',
            'download_url': download_url
        })
    }
