from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
import os
from dotenv import load_dotenv

# Loading variables from .env file
load_dotenv()

DB_URL = os.getenv("POSTGRES_CONNECTION")

# Initialize Database and Metadata
database = Database(DB_URL)
metadata = MetaData()

# Define Tables
system_prompt = Table(
    "system_prompt",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("systemPrompt", String, unique=True, nullable=False, index=True),
)

ai_model = Table(
    "ai_model",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("aiModel", String, unique=True, nullable=False, index=True),
)

content_prompt = Table(
    "content_prompt",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("contentPrompt", String, nullable=False, index=True),
    Column("aiModel_id", Integer, ForeignKey("ai_model.id"), nullable=False),
    Column("systemPrompt_id", Integer, ForeignKey("system_prompt.id"), nullable=False)
)

llm_grader = Table(
    "llm_grader",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("systemPrompt_id", Integer, ForeignKey("system_prompt.id"), nullable=False),
    Column("contentPrompt_id", Integer, ForeignKey("content_prompt.id"), nullable=False),
    Column("aiModel_id", Integer, ForeignKey("ai_model.id"), nullable=False),
    Column("response", String, nullable=False),
    Column("score", Float, nullable=True),  # Optional grading score
)

# Database Engine
engine = create_engine(DB_URL)

# Create Tables
metadata.create_all(engine)
