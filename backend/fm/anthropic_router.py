import boto3
import json
import logging

logger = logging.getLogger('uvicorn.error')

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

def invoke(prompt, temp=0.5,  max_tokens=1024):
    prompt_config = {
        "max_tokens": max_tokens,
        "system": "Always Verify your technical answer or say it if you are not sure. Use AWS documentation as reference if context needed",
        "temperature": temp,
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": f'{prompt}',
            }
        ],
    }
    model_id = "arn:aws:bedrock:us-east-1:601156590858:default-prompt-router/anthropic.claude:1"

    response = bedrock_runtime.invoke_model(
        body=json.dumps(prompt_config),
        modelId=model_id
    )

    response_body = json.loads(response.get("body").read())

    logger.debug(f"Full response (metadata): {response['ResponseMetadata']}")
    logger.debug(f"Full response (body): {json.dumps(response_body, indent=2)}")
    logger.info(f"Stop reason: {json.dumps(response_body['stop_reason'])}")
    logger.info(f"Model Used: {json.dumps(response_body['model'])}")
    logger.info(f"Tokens used by {model_id}: {json.dumps(response_body['usage'])}")
    logger.info(f"Latency: {response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-invocation-latency']}")

    return response_body["content"][0]["text"]
