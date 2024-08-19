"""From control-plane/app/pydantic_models/openai.py"""

from enum import StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Any, Dict, List

from openai import Client
from openai.types import Completion
from openai.types.chat import ChatCompletion

__all__ = [
    "Client",
    "Completion",
    "ChatCompletion",
    "ChatCompletionRequest",
    "CompletionRequest",
]

BaseModel.model_config["protected_namespaces"] = ()


class RoleEnum(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: RoleEnum
    content: str


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = Field(description="Bookend Model ID")
    frequency_penalty: float | None = Field(default=None, ge=-2.0, le=2.0)
    logit_bias: Dict[str, int] | None = None
    logprobs: bool | None = False
    top_logprobs: int | None = None
    max_tokens: int | None = None
    n: int | None = 1
    presence_penalty: float | None = Field(default=None, ge=-2.0, le=2.0)
    response_format: Dict[str, str] | None = None
    seed: int | None = None
    service_tier: str | None = None
    stop: str | List[str] | None = None
    stream: bool | None = False
    stream_options: Dict[str, bool] | None = None
    temperature: float | None = Field(default=None, ge=0, le=2.0)
    top_p: float | None = Field(default=None, ge=0, le=2.0)
    tools: List[Dict[str, Any]] | None = None
    tool_choice: str | Dict[str, Any] | None = None
    parallel_tool_calls: bool | None = None
    user: str | None = None

    @field_validator("response_format")
    @classmethod
    def response_format_value(
        cls, response_format: Dict[str, str] | None
    ) -> Dict[str, str] | None:
        if not response_format:
            return None
        if len(response_format) == 1 and response_format.get("type") in [
            "text",
            "json_object",
        ]:
            return response_format
        raise ValidationError(
            "`response_format` must be `None` or have `type` field set to one of `text` or `json_object`."
        )


class CompletionRequest(BaseModel):
    model: str
    prompt: str | List[Any]
    suffix: str | None = None
    temperature: float = 0.7
    n: int = 1
    max_tokens: int = 16
    stop: str | List[str] | None = None
    stream: bool = False
    top_p: float = 1.0
    top_k: int = -1
    logprobs: int | None = None
    echo: bool = False
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    user: str | None = None
