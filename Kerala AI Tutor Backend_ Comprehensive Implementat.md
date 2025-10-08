<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Kerala AI Tutor Backend: Comprehensive Implementation Document for Cursor Editor AI


***

## Overview

This document provides a complete production-ready backend implementation for Kerala AI Tutor, an AI-powered tutoring platform designed to provide instant, curriculum-aligned answers based on SCERT Kerala syllabus content.

The backend leverages FastAPI as the web framework, PostgreSQL for storing structured syllabus metadata, Pinecone for semantic retrieval over embedded syllabus content, and OpenAI's large language models for generating tailored student responses. LangChain is used as a flexible interface to bridge subsystems (optional expansion).

***

## System Architecture

```
 ┌───────────────┐       HTTP/JSON       ┌───────────────┐
 │   Frontend    │  <----------------->  │ FastAPI Backend│
 │ (React, Next) │                      │               │
 └───────────────┘                      └─────┬─────────┘
                                              │
                ┌─────────────────────────────┴──────────────────────────┐
                │                                                         │
      ┌──────────────────┐                                    ┌───────────────────┐
      │  PostgreSQL DB   │                                    │   Pinecone DB     │
      │ (syllabus tables)│                                    │ (vector embeddings)│
      └──────────────────┘                                    └───────────────────┘
                                                                   │
                                                     ┌─────────────┴─────────────┐
                                                     │ OpenAI / GPT or LLM Model │
                                                     └───────────────────────────┘
```


***

## 1. Folder Structure

```
kerala_ai_tutor/
 ┣ backend/
 ┃ ┣ main.py                  # FastAPI app with Q&A route
 ┃ ┣ embeddings.py            # Embedding generation & Pinecone upsert
 ┃ ┣ models.py                # SQLAlchemy DB definitions (classes, subjects, chapters, ... )
 ┃ ┣ db.py                    # DB connection management
 ┃ ┣ requirements.txt         # Python package dependencies
 ┃ ┣ .env.example             # Environment variables example
 ┃ ┗ README.md                # Setup, usage, API doc
 ┣ data/
 ┃ ┗ class_10/                # Example syllabus PDF/text data
 ┗ frontend/
   ┗ react-app/                # Your React frontend app
```


***

## 2. Environment Configuration (`.env.example`)

```bash
OPENAI_API_KEY=your-openai-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-east-1

POSTGRES_DB=tutor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpass
POSTGRES_HOST=localhost
```


***

## 3. Database Models (`models.py`)

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_id = Column(Integer, ForeignKey('classes.id'))

class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject_id = Column(Integer, ForeignKey('subjects.id'))

class Section(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    chapter_id = Column(Integer, ForeignKey('chapters.id'))

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text)
    answer_text = Column(Text)
    section_id = Column(Integer, ForeignKey('sections.id'))
```


***

## 4. Database Connection (`db.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```


***

## 5. Embedding Logic (`embeddings.py`)

```python
import os
from openai import OpenAI
from pinecone import Pinecone
import psycopg2

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("kerala-ai-tutor")

def embed_and_store():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM sections;")
    data = cursor.fetchall()

    for section_id, text in data:
        if not text.strip():
            continue
        emb = client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding
        index.upsert(vectors=[(str(section_id), emb, {"text": text})])
```


***

## 6. FastAPI Backend with AI Question Answering (`main.py`)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from pinecone import Pinecone
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("kerala-ai-tutor")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask/")
def ask_question(req: QuestionRequest):
    try:
        q_embed = client.embeddings.create(
            model="text-embedding-3-small",
            input=req.question
        ).data[0].embedding

        results = index.query(vector=q_embed, top_k=3, include_metadata=True)
        context = "\n".join([m["metadata"]["text"] for m in results["matches"]])

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI tutor for Kerala SCERT students (Classes 8–12)."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {req.question}"}
            ]
        )

        answer = response.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```


***

## 7. Running the Backend

1. Install dependencies:
`pip install -r requirements.txt`
2. Set environment variables (copy `.env.example` to `.env` and fill your keys).
3. Initialize PostgreSQL database and tables (run models or migrate).
4. Generate embeddings from syllabus content:
`python embeddings.py`
5. Start FastAPI server:
`uvicorn main:app --reload`
6. Test querying:
```
POST /ask/
{
  "question": "Explain Ohm’s Law from Class 10 Physics"
}
```


***

## 8. Frontend Integration

- Frontend calls `/ask/` endpoint with JSON body `{ "question": "<student question>" }`.
- Display returned `answer` in chat interface.
- Optionally show context metadata.

Example fetch:

```js
const response = await fetch("https://api.yourdomain.com/ask/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "What is a linear equation?" }),
});
const data = await response.json();
console.log(data.answer);
```


***

## 9. Scaling \& Optimization Tips

- Use Redis caching for repeated queries.
- Process and embed syllabus content in batches.
- Add multilingual support by pre-translating or separately embedding Malayalam and English content.
- Fine-tune AI models on local SCERT Q\&A data for improved accuracy.
- Track user analytics in PostgreSQL.

***

## Summary

- **Data Layer:** PostgreSQL stores structured syllabus metadata.
- **Vector Store:** Pinecone stores semantic embeddings of syllabus content.
- **AI Layer:** OpenAI GPT or other LLMs answer queries using retrieved context.
- **API Layer:** FastAPI serves AI Q\&A endpoints efficiently.
- **Frontend:** React or React Native communicates with backend for real-time Q\&A.

This architecture is scalable, flexible, and tuned for Kerala's education ecosystem. Ready for direct implementation with Cursor editor AI or similar code-first tools.

***

Would you like me to generate the full complete backend folder with the above components for you now?

