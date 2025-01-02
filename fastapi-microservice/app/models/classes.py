
from groq import BaseModel


class AIRequestBody(BaseModel):
    systemPrompt: str | None = (
        "you are a funny person and you explain stuff in a fun way"
    )
    contentPrompt: str | None = {"explain suny oswego"}


class AIResponseBody(BaseModel):
    systemPrompt: str | None = None
    contentPrompt: str | None = None
    response: str | None = None
    aiModel: str| None = None
    
    
class DataResponseBody(BaseModel):
    systemPrompt: str | None = None
    contentPrompt: str | None = None
    aiModel: str| None = None
    response: str | None = None
    score: str | None = None
    
class DataSystemPromptResponseBody(BaseModel):
    systemPrompt: str | None = None
    id: int | None = None