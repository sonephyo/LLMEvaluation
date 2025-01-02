from typing import List
from groq import BaseModel, Groq
from dotenv import load_dotenv
import os
from sqlalchemy import text
from app.soney_llm_postgres import (
    database,
    system_prompt,
    content_prompt,
    llm_grader,
    ai_model,
)
from app.models.classes import (
    AIRequestBody,
    AIResponseBody,
    DataSystemPromptResponseBody,
)

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")


client = Groq(
    api_key=groq_key,
)


async def generateResponse(requestBody: AIRequestBody) -> List[AIResponseBody]:

    ai_model_list = ["llama3-8b-8192", "gemma2-9b-it"]

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

        sql = text(
            f"""SELECT llm_grader.*, content_prompt.*, system_prompt.*, ai_model.*
                FROM llm_grader
                JOIN content_prompt ON content_prompt.id = {content_prompt_id}
                JOIN system_prompt ON system_prompt.id = {system_prompt_id}
                JOIN ai_model ON ai_model.id = {ai_model_id}
                WHERE llm_grader.id = {last_response_id}"""
        )
        inserted_response = await database.fetch_one(sql)

        dict_result = dict(inserted_response)

        responseInstance = AIResponseBody(
            systemPrompt=dict_result.get("systemPrompt"),
            contentPrompt=dict_result.get("contentPrompt"),
            response=dict_result.get("response"),
            aiModel=dict_result.get("aiModel"),
        )
        responseData.append(responseInstance)

    return responseData


async def getSystemPrompts() -> List[DataSystemPromptResponseBody]:
    """
    Returns:
        List[DataSystemPromptResponseBody]: SystemPrompts with its id
    """

    system_promptResponse = system_prompt.select()
    responses = await database.fetch_all(system_promptResponse)

    output: List[DataSystemPromptResponseBody] = []
    for response in responses:
        response_dict = dict(response)
        print(response_dict)
        output.append(
            DataSystemPromptResponseBody(
                id =response_dict.get("id"),
                systemPrompt=response_dict.get("systemPrompt"),
            )
        )

    return output
