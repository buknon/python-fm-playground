import boto3
import json

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

def invoke(prompt, temp=0.5,  max_tokens=1024):
    systemPrompt = """
                    Always Verify your technical answer or say it if you are not sure. Use AWs documentation as reference
                   """;

    prompt_config = {
        "max_tokens": max_tokens,
        "temperature": temp,
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": f'{systemPrompt}\n\n{prompt}'}],
            }
        ],
    }
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    response = bedrock_runtime.invoke_model(
        body=json.dumps(prompt_config),
        modelId=model_id
    )

    response_body = json.loads(response.get("body").read())


    return response_body["content"][0]["text"]
