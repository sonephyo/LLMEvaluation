from typing import List
from fastapi import APIRouter
from sqlalchemy import text
from app.services.llm_data_storage_service import getData
from app.soney_llm_postgres import (
    database,
    system_prompt,
    content_prompt,
    llm_grader,
    ai_model,
)
from app.models.classes import DataResponseBody

router = APIRouter(
    prefix="/data",
)


@router.get("/", response_model=List[DataResponseBody])
async def get_LLM_data():
    """Getting all LLM generated data

    :return: all response data
    """
    return await getData()
