from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
import os
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()

DB_URL = os.getenv("POSTGRES_CONNECTION")

database = Database(DB_URL)
metadata = MetaData()

llm_data = Table (
  "llm_data",
  metadata,
  Column("id", Integer, primary_key=True, index=True),
  Column("systemPrompt", String, index=True),
  Column("contentPrompt", String, index=True),
  Column("response", String, index= True),
)

engine = create_engine(DB_URL)
metadata.create_all(engine)