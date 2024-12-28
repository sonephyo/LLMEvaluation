from groq import BaseModel, Groq
from fastapi import APIRouter
from dotenv import load_dotenv
import os
from app.services.llm_generator_service import generateResponse, getAllResponses

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

class AIRequestBody(BaseModel):
    systemPrompt: str | None = (
        "you are a funny person and you explain stuff in a fun way"
    )
    contentPrompt: str | None = {
        "explain suny oswego"
    }

class AIResponseBody(BaseModel):
    systemPrompt: str | None = None
    contentPrompt: str | None = None
    response: str | None = None

router = APIRouter(
    prefix="/ai",
)

@router.post("/", response_model=AIResponseBody)
async def use_LLM(requestBody: AIRequestBody):
    """Generating a request from LLM

    :param requestBody: requestBody include systemPrompt(optional) and contentPrompt(required)
    :return: generated response from "llama3-8b-8192"
    """
    return await generateResponse(requestBody)

@router.get("/responses")
async def get_all_responses():
    return await getAllResponses()
