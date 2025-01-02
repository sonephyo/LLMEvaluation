from typing import List
from groq import BaseModel, Groq
from fastapi import APIRouter
from dotenv import load_dotenv
import os
from app.services.llm_generator_service import generateResponse
from app.models.classes import AIRequestBody, AIResponseBody

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

router = APIRouter(
    prefix="/ai",
)


@router.post("/", response_model=List[AIResponseBody])
async def use_LLM(requestBody: AIRequestBody):
    """Generating a request from LLM

    :param requestBody: requestBody include systemPrompt(optional) and contentPrompt(required)
    :return: generated response from "llama3-8b-8192"
    """
    return await generateResponse(requestBody)
