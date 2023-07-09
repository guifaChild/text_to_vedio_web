from fastapi import APIRouter, UploadFile

from midjourney.lib.api import discord
from midjourney.lib.api.discord import TriggerType
from midjourney.util._queue import taskqueue
from .handler import prompt_handler
from .schema import (
    TriggerImagineIn,
    TriggerResponse
)

router = APIRouter()


@router.post("/imagine", response_model=TriggerResponse)
async def imagine(body: TriggerImagineIn):

    trigger_id, prompt = prompt_handler(body.prompt, body.picurl)
    trigger_type = TriggerType.generate.value

    taskqueue.put(trigger_id, discord.generate, prompt)
    return {"trigger_id": trigger_id, "trigger_type": trigger_type}

