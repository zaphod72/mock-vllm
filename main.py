import asyncio
import json
import time
from typing import Any, Callable, Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from uuid import uuid4
from pydantic_models import ChatCompletionRequest, ChatMessage, CompletionRequest, RoleEnum

app = FastAPI(title="OpenAI-compatible API")


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    def make_message(i: int, token: str) -> Dict[str, str | ChatMessage]:
        return {"index": str(i), "message": ChatMessage(role=RoleEnum.ASSISTANT, content=token)}

    if request.messages:
        resp_content = f"As a mock AI Assitant, I can only echo your last message: {request.messages[-1].content}"
    else:
        resp_content = "As a mock AI Assitant, I can only echo your last message, but there wasn't one!"
    return _completions(request, resp_content, make_message)


@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    def make_message(i: int, token: str) -> Dict[str, str | ChatMessage]:
        return {"index": str(i), "text": token}

    if request.prompt:
        resp_content = (
            f"As a mock AI Assitant, I can only echo your prompt: {request.prompt}"
        )
    else:
        resp_content = (
            "As a mock AI Assitant, I can only echo your prompt, but there wasn't one!"
        )
    return _completions(request, resp_content, make_message)


async def _completions(
    request: CompletionRequest | ChatCompletionRequest,
    resp_content: str,
    make_message: Callable[[int, str], Dict[str, str | ChatMessage]],
):
    data = {
        "id": uuid4(),
        "object": "text_completion"
        if isinstance(request, CompletionRequest)
        else "chat.completion",
        "created": time.time(),
        "model": request.model,
    }
    if request.stream:
        return StreamingResponse(
            _async_generator(resp_content, data, make_message),
            media_type="text/event-stream",
        )

    message = make_message(0, resp_content)
    message["finish_reason"] = "stop"
    data["choices"] = [message]
    return data


async def _async_generator(
    text_resp: str, data: Dict[str, Any], choices: Callable[[int, str], Dict[str, str | ChatMessage]]
):
    # let's pretend every word is a token and return it over time
    tokens = text_resp.split(" ")

    for token in tokens:
        data["choices"] = [choices(0, token)]
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(0.5)
    yield "data: [DONE]\n\n"


@app.get("/test")
def test():
    return {"message": "Test successful"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
