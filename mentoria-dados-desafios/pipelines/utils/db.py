import os
from sqlalchemy import create_engine

DB_URL = os.getenv('DB_URL', 'postgresql://postgres:postgres@localhost:5432/mentoria_dados')
engine = create_engine(DB_URL)

def get_connection():
    return engine.connect()

def get_engine():
    return engine
