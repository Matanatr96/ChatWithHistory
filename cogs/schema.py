from pydantic import BaseModel


class ChatRequest(BaseModel):
    messages: list[dict]
    temperature: float = 0.2
    max_tokens: int = 256
    stop: list[str] = []
    stream: bool = False


class ChatResponse(BaseModel):
    choices: list[dict]


class ChatbotAPIError(Exception):
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code  # HTTP status code (if available)
        self.response_data = response_data  # Response data from the API (if available)

    def __str__(self):
        error_message = super().__str__()
        if self.status_code is not None:
            error_message += f" (HTTP Status Code: {self.status_code})"
        return error_message
