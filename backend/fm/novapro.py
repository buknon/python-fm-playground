import boto3
import logging
import json 

logger = logging.getLogger('uvicorn.error')


bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

def invoke(prompt, temp=0.5,  max_tokens=1024):
    systemPrompt = [{"text": "Always Verify your technical answer or say it if you are not sure. Use AWs documentation as reference"}]
    
    messages = [
        {"role": "user", "content": [{"text": f'{prompt}'}]}    ,
    ]

    inf_params = {"maxTokens": max_tokens, "temperature": temp}

    additionalModelRequestFields = {
        "inferenceConfig": {
         "topK": 50
        }
}


    model_id = "us.amazon.nova-pro-v1:0"

    response = bedrock_runtime.converse(
        messages=messages,
        additionalModelRequestFields=additionalModelRequestFields,
        inferenceConfig=inf_params,
        modelId=model_id,
        system=systemPrompt
    )

    logger.debug(f"Full response: \n{json.dumps(response, indent=2)}")
    logger.info(f"Stop reason: {response['stopReason']}")
    logger.info(f"Tokens used by {model_id}: {response['usage']}")
    logger.info(f"Latency: {response['metrics']['latencyMs']}")

    return response["output"]["message"]["content"][0]["text"]
