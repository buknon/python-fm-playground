import sys
sys.path.append("../fm")


from fastapi import APIRouter, HTTPException
from botocore.exceptions import ClientError
from . import models
from . import services

from fm import claude3

router = APIRouter()


@router.post("/foundation-models/model/chat/anthropic.claude-v2/invoke")
def invoke(body: models.ChatRequest):
    try:
        completion = services.invoke(body.prompt)
        return models.ChatResponse(
            completion=completion
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDeniedException":
            raise HTTPException(status_code=403)
        else:
            raise HTTPException(status_code=500)

@router.post("/foundation-models/model/chat/anthropic.claude-v3/invoke")
def invoke(body: models.ChatRequest):
    try:
        completion = claude3.invoke(body.prompt)
        return models.ChatResponse(
            completion=completion
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDeniedException":
            raise HTTPException(status_code=403)
        else:
            raise HTTPException(status_code=500)