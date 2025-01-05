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


def evaluateResponse(data_dict: dict):
    evaluation_metrics = [
        "isValid: boolean",
        "accuracy: number",
        "correctness: number",
        "relevancy: number",
    ]
    contentTemplate: str = f"""
    Input: {data_dict.get("systemPrompt")}
    Output: {data_dict.get("contentPrompt")}
    """
    for metric in evaluation_metrics:
        systemTemplate: str = f"""
        Output only the number out of 10. Do not write any texts
        Criteria - {metric}
        """

        if metric == "isValid: boolean":
            systemTemplate: str = f"""
        Output only true or false. Do not write any texts
        Criteria - {metric}
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": systemTemplate},
                {
                    "role": "user",
                    "content": contentTemplate,
                },
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        response_content = chat_completion.choices[0].message.content
        print(metric, response_content)
