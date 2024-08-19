import asyncio
import json
import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from pydantic_models import ChatCompletionRequest, ChatMessage, CompletionRequest

app = FastAPI(title="OpenAI-compatible API")


async def _chat_completions_async_generator(text_resp: str, model: str):
    # let's pretend every word is a token and return it over time
    tokens = text_resp.split(" ")

    for i, token in enumerate(tokens):
        chunk = {
            "id": i,
            "object": "chat.completion.chunk",
            "created": time.time(),
            "model": model,
            "choices": [
                {
                    "index": i,
                    "delta": {"content": token + " "},
                }
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(1)
    yield "data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.messages:
        resp_content = f"As a mock AI Assitant, I can only echo your last message: {request.messages[-1].content}"
    else:
        resp_content = "As a mock AI Assitant, I can only echo your last message, but there wasn't one!"
    if request.stream:
        return StreamingResponse(
            _chat_completions_async_generator(resp_content, request.model),
            media_type="text/event-stream",
        )

    id = str(time.time())
    return {
        "id": id,
        "object": "chat.completion",
        "created": id,
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": ChatMessage(role="assistant", content=resp_content),
                "finish_reason": "stop",
            }
        ],
    }


async def _completions_async_generator(text_resp: str, model: str):
    # let's pretend every word is a token and return it over time
    tokens = text_resp.split(" ")

    for i, token in enumerate(tokens):
        chunk = {
            "id": i,
            "created": time.time(),
            "model": model,
            "choices": [
                {
                    "index": i,
                    "text": token,
                }
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(1)
    yield "data: [DONE]\n\n"


@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    if request.prompt:
        resp_content = (
            f"As a mock AI Assitant, I can only echo your prompt: {request.prompt}"
        )
    else:
        resp_content = (
            "As a mock AI Assitant, I can only echo your prompt, but there wasn't one!"
        )
    if request.stream:
        return StreamingResponse(
            _completions_async_generator(resp_content, request.model),
            media_type="text/event-stream",
        )

    id = str(time.time())
    return {
        "id": id,
        "created": id,
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "text": resp_content,
                "finish_reason": "stop",
            }
        ],
    }


@app.get("/test")
def test():
    return {"message": "Test successful"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
