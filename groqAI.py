import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router =  APIRouter()

class ExpenseItem(BaseModel):
    amount: float
    category: str
    date: str

class AIRequest(BaseModel):
    question: str
    expenses: List[ExpenseItem]

@router.post("/ask-ai")
def ask_ai(data: AIRequest):
    prompt = f"""
You are a financial advisor. Analyze the following expenses and answer the question: "{data.question}"

Expenses:
{[{"amount": e.amount, "category": e.category, "date": e.date} for e in data.expenses]}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful finance expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="AI request failed")

    return {"response": response.json()["choices"][0]["message"]["content"]}
