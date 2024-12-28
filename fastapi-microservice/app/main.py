from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import BaseModel, Groq
import os
from app.soney_llm_postgres import database, llm_grader
from app.routers.llm_generator import router as llm_generator_router

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

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(llm_generator_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI microservice"}