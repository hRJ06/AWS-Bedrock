import json
import boto3

def lambda_handler(event, context):
    try:
        user_query = event.get('query');
        bedrock = boto3.client('bedrock-agent-runtime')
        response = bedrock.retrieve_and_generate(
            input={
                'text': user_query
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE', 
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': '<YOUR_KNOWLEDGE_BASE_ID>', 
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0'
                }
            }
        )
        answer = response['output']['text']
        citations = []
        for citation in response.get("citations", []):
            for ref in citation.get("retrievedReferences", []):
                text = ref.get("content", {}).get("text")
                if text:
                    citations.append(text.strip())
        return {
            'statusCode': 200,
            'body': json.dumps({
                'answer': answer,
                'citations': citations
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                'error': str(e)
            })
        }
    
