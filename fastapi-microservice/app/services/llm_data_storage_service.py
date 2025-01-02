from typing import List
from groq import BaseModel, Groq
from dotenv import load_dotenv
import os
from sqlalchemy import select
from app.soney_llm_postgres import (
    database,
    system_prompt,
    content_prompt,
    llm_grader,
    ai_model,
)
from app.models.classes import DataResponseBody

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


client = Groq(
    api_key=groq_key,
)


async def getData() -> List[DataResponseBody]:
    join_condition = (
        llm_grader
        .join(content_prompt, llm_grader.c.contentPrompt_id == content_prompt.c.id)
        .join(system_prompt, llm_grader.c.systemPrompt_id == system_prompt.c.id)
        .join(ai_model, llm_grader.c.aiModel_id == ai_model.c.id)
    )

    query = select(
        llm_grader,
        content_prompt, 
        system_prompt, 
        ai_model,
    ).select_from(join_condition)

    output: List[DataResponseBody] = []
    database_response = await database.fetch_all(query)
    for response in database_response:
        response_dict = dict(response)
        
        output.append(DataResponseBody(
            systemPrompt=response_dict.get("systemPrompt"),
            contentPrompt=response_dict.get("contentPrompt"),
            response=response_dict.get("response"),
            aiModel=response_dict.get("aiModel"),
            score=response_dict.get("score")
        ))
        
    return output
        
    

