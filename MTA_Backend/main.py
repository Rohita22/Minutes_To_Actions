#minimal server --> enabled CORS so that the frontend can talk to the backend

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, insert_session, list_sessions, get_session
from schemas import SessionCreate
import json
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize DB when app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)  #creats fast api web server inst

app.add_middleware( #called middleware as it sits in the middle of browser to fastapi and fastapi to browser
    CORSMiddleware, #b4 anything reach /health CORS middleware checks is it coming from authentic origin
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #basically allows frontend running on port 3000 and 5173 to make requests to the backend

@app.get("/health") #endpoint is health
def health():
    return {"status": "ok"}
#used to check if the backend is still alive or not


#.\.venv\Scripts\Activate.ps1 to activate vir env
# python -m uvicorn main:app --reload --port 8000 to see the webpage


def generate_with_llm(notes: str):

    prompt = f"""
You are an enterprise meeting minutes extractor. 
If summary is one paragraph, split it into bullet-style sentences.
Each element in summary MUST be a separate array item.
Each element in decisions MUST be a separate array item.


STRICT RULES:
- Return ONLY raw valid JSON.
- No markdown.
- No explanations.
- Do NOT infer missing information.
- If something is not explicitly mentioned, leave it null or empty.

Schema:

{{
  "summary": ["string"],
  "decisions": ["string"],
  "action_items": [
    {{
      "owner": "string",
      "task": "string",
      "due_date": null,
      "priority": null
    }}
  ]
}}

Meeting notes:
{notes}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    output_text = response.choices[0].message.content.strip()

    # Remove accidental markdown if model adds it
    if output_text.startswith("```"):
        output_text = output_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(output_text)
        return validate_structure(parsed)
    except Exception as e:
        print("RAW MODEL OUTPUT:", output_text)
        raise Exception(f"Invalid JSON returned by model: {e}")

def validate_structure(data: dict):

    data.setdefault("summary", [])
    data.setdefault("decisions", [])
    data.setdefault("action_items", [])

    # FORCE summary to be array
    if isinstance(data["summary"], str):
        data["summary"] = [data["summary"]]

    # FORCE decisions to be array
    if isinstance(data["decisions"], str):
        data["decisions"] = [data["decisions"]]

    # Ensure summary items are strings
    data["summary"] = [
        str(s) for s in data["summary"]
    ]

    # Ensure decisions items are strings
    data["decisions"] = [
        str(d) for d in data["decisions"]
    ]

    # Normalize action items
    normalized_items = []
    for item in data["action_items"]:
        normalized_items.append({
            "owner": item.get("owner", ""),
            "task": item.get("task", ""),
            "due_date": item.get("due_date", None),
            "priority": item.get("priority", None),
        })

    data["action_items"] = normalized_items

    return data


@app.post("/sessions")
def create_session(payload: SessionCreate):
    title = payload.title or "Untitled Meeting"

    try:
        generated = generate_with_llm(payload.notes)
    except Exception as e:
        print("LLM ERROR:", e)
        generated = {
            "summary": ["AI generation failed."],
            "decisions": [],
            "action_items": []
        }

    session_id = insert_session(
        title=title,
        notes=payload.notes,
        summary=generated["summary"],
        decisions=generated["decisions"],
        action_items=generated["action_items"],
    )

    saved = get_session(session_id)

    return {
        "session_id": saved["id"],
        "title": saved["title"],
        "created_at": saved["created_at"],
        "summary": saved["summary"],
        "decisions": saved["decisions"],
        "action_items": saved["action_items"],
    }

