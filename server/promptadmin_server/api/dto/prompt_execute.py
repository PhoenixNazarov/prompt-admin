from promptadmin.prompt_service.models.anthropic import AnthropicModelResponse
from promptadmin.types import ModelResponse
from pydantic import BaseModel


class PromptExecute(BaseModel):
    response_model: AnthropicModelResponse | ModelResponse
    parsed_model_error: bool
