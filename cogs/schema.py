from pydantic import BaseModel

class ChatRequest(BaseModel):
    messages: list[dict]
    stop: list[str]
    temperature: float
    max_tokens: int
    stream: bool

class ChatResponse(BaseModel):
    choices: list[dict]


class ChatbotAPIError(Exception):
    pass