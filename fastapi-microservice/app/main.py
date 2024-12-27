from contextlib import asynccontextmanager
from fastapi import FastAPI
from groq import BaseModel, Groq
import os
from app.soney_llm_postgres import database, llm_data


from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=groq_key,
)

# Classes for request body
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await database.connect()
    yield
    # Clean up the ML models and release the resources
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI microservice"}


@app.get("/items/{item_id}/{q}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/ai", response_model=AIRequestBody)
async def use_LLM(requestBody: AIRequestBody):
    """Generating a request from LLM

    :param requestBody: requestBody include systemPrompt(optional) and contentPrompt(required)
    :return: generated response from "llama3-8b-8192"
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": requestBody.systemPrompt},
            {
                "role": "user",
                "content": requestBody.contentPrompt,
            },
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    
    query = llm_data.insert().values(contentPrompt=requestBody.contentPrompt, systemPrompt=requestBody.systemPrompt, response=chat_completion.choices[0].message.content)
    last_response_id = await database.execute(query)
    
    query = llm_data.select().where(llm_data.c.id == last_response_id)
    inserted_response = await database.fetch_one(query)
    return inserted_response
    
    
