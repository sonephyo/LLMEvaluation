from collections import defaultdict
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import BaseModel, Groq
import os
from app.soney_llm_postgres import database, llm_grader
from app.routers.llm_generator import router as llm_generator_router
from app.routers.llm_data_storage import router as llm_data_storage_router

from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=groq_key,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await database.connect()
    yield
    # Clean up the ML models and release the resources
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "http://localhost:4173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limits = defaultdict(list)
MAX_REQUESTS = 1
TIME_WINDOW = 60


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    print("ahsd;kljfh;askdjf", request.url.path)
    if request.url.path == "/ai/" and request.method == "POST":
        client_ip = request.client.host
        current_time = time.time()

        # Initialize rate limits for the client IP if not already set
        if client_ip not in rate_limits:
            rate_limits[client_ip] = []

        # Remove expired timestamps
        rate_limits[client_ip] = [
            timestamp
            for timestamp in rate_limits[client_ip]
            if current_time - timestamp < TIME_WINDOW
        ]

        # Check if the request exceeds the rate limit
        if len(rate_limits[client_ip]) >= MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Too many requests")

        # Allow the request
        rate_limits[client_ip].append(current_time)

    response = await call_next(request)
    return response


app.include_router(llm_generator_router)
app.include_router(llm_data_storage_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI microservice"}
