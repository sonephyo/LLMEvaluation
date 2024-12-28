from typing import List
from groq import BaseModel, Groq
from fastapi import APIRouter
from dotenv import load_dotenv
import os
from app.soney_llm_postgres import (
    database,
    system_prompt,
    content_prompt,
    llm_grader,
    ai_model,
)

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


class AIRequestBody(BaseModel):
    systemPrompt: str | None = (
        "you are a funny person and you explain stuff in a fun way"
    )
    contentPrompt: str | None = {"explain suny oswego"}


class AIResponseBody(BaseModel):
    systemPrompt: str | None = None
    contentPrompt: str | None = None
    response: str | None = None


client = Groq(
    api_key=groq_key,
)


async def generateResponse(requestBody: AIRequestBody) -> List[AIResponseBody]:

    ai_model_list = ["llama3-8b-8192", "llama-guard-3-8b"]

    responseData: List[AIResponseBody] = []

    for ai_model_ind in ai_model_list:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": requestBody.systemPrompt},
                {
                    "role": "user",
                    "content": requestBody.contentPrompt,
                },
            ],
            model=ai_model_ind,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        response_content = chat_completion.choices[0].message.content

        system_prompt_query = system_prompt.select().where(
            system_prompt.c.systemPrompt == requestBody.systemPrompt
        )
        existing_system_prompt = await database.fetch_one(system_prompt_query)

        if existing_system_prompt:
            system_prompt_id = existing_system_prompt["id"]
        else:
            system_prompt_insert_query = system_prompt.insert().values(
                systemPrompt=requestBody.systemPrompt
            )
            system_prompt_id = await database.execute(system_prompt_insert_query)

        # Insert or get AI model
        ai_model_query = ai_model.select().where(ai_model.c.aiModel == ai_model_ind)
        existing_ai_model = await database.fetch_one(ai_model_query)

        if existing_ai_model:
            ai_model_id = existing_ai_model["id"]
        else:
            ai_model_insert_query = ai_model.insert().values(aiModel=ai_model_ind)
            ai_model_id = await database.execute(ai_model_insert_query)

        # Insert or get contentPrompt
        content_prompt_query = content_prompt.select().where(
            (content_prompt.c.contentPrompt == requestBody.contentPrompt)
            & (content_prompt.c.systemPrompt_id == system_prompt_id)
        )
        existing_content_prompt = await database.fetch_one(content_prompt_query)

        if existing_content_prompt:
            content_prompt_id = existing_content_prompt["id"]
        else:
            content_prompt_insert_query = content_prompt.insert().values(
                contentPrompt=requestBody.contentPrompt,
                systemPrompt_id=system_prompt_id,
                aiModel_id=ai_model_id,
            )
            content_prompt_id = await database.execute(content_prompt_insert_query)

        # Insert response into llm_grader
        llm_grader_insert_query = llm_grader.insert().values(
            systemPrompt_id=system_prompt_id,
            contentPrompt_id=content_prompt_id,
            aiModel_id=ai_model_id,
            response=response_content,
        )
        last_response_id = await database.execute(llm_grader_insert_query)

        # Fetch the inserted response
        response_query = llm_grader.select().where(llm_grader.c.id == last_response_id)
        inserted_response = await database.fetch_one(response_query)

        responseData.append(inserted_response)
        
    return responseData


async def getAllResponses() -> List[AIResponseBody]:

    query = llm_data.select()
    responses = await database.fetch_all(query)
    print(responses)
    return [AIResponseBody(**dict(row)) for row in responses]
