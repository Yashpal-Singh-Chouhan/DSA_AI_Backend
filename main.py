from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AssessmentRequest(BaseModel):
    answers: dict


class LessonRequest(BaseModel):
    profile: dict
    topic: str


@app.get("/")
def home():
    return {
        "message": "DSA AI Backend Running Successfully"
    }


@app.post("/generate-profile")
def generate_profile(data: AssessmentRequest):

    prompt = f"""
You are Madhav, an expert DSA mentor.

Analyze the following student assessment answers:

{data.answers}

Return ONLY valid JSON.

Format:

{{
  "learnerType": "",
  "mentorStyle": "",
  "strength": "",
  "weakness": "",
  "roadmap": []
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    text = text.strip()

    try:
        profile = json.loads(text)
        return profile

    except:
        return {
            "learnerType": "Balanced Learner",
            "mentorStyle": "Adaptive Mode",
            "strength": "Good Learning Ability",
            "weakness": "Needs More Practice",
            "roadmap": [
                "Arrays",
                "Strings",
                "Linked Lists",
                "Trees",
                "Graphs"
            ]
        }


@app.post("/generate-lesson")
def generate_lesson(data: LessonRequest):

    prompt = f"""
You are Madhav, an expert DSA mentor.

Student Profile:

{data.profile}

Teach the topic:

{data.topic}

Rules:

1. Use real life examples.
2. Use visual explanations.
3. Explain WHY before HOW.
4. Use simple language.
5. Use diagrams wherever possible.
6. Give one small exercise at the end.

Return only lesson text.
"""

    response = model.generate_content(prompt)

    return {
        "lesson": response.text
    }