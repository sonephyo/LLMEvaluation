from typing import List
from fastapi import APIRouter
from app.services.llm_generator_service import generateResponse, getSystemPrompts
from app.models.classes import AIRequestBody, AIResponseBody, DataSystemPromptResponseBody

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

@router.get("/systemPrompts", response_model=List[DataSystemPromptResponseBody])
async def getAllSystemPrompts():
    """Get all systemPrompts generated
    
    :return: list of all System prompts
    """
    return await getSystemPrompts()