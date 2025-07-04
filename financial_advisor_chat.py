# Import the necessary libraries
from fastapi.responses import FileResponse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os


try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    exit()

# --- THE AGENT'S "BRAIN" ---
# Initialize the Generative Model. 'gemini-1.5-flash' is a great, versatile model.
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()


class ChatRequest(BaseModel):
    history: list[str]  # Each item is a message (user or AI)

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Combine advisor context and chat history
        advisor_context = (
            "Please format your responses using Markdown for clarity (use headings, bold, bullet points, etc.)."
            "You are a helpful, knowledgeable, and ethical financial advisor. "
            "You provide clear, accurate, and responsible financial advice, "
            "but you do not give investment, legal, or tax advice. "
            "Always remind users to consult a certified professional for major decisions."
        )
        prompt = advisor_context + "\n" + "\n".join(request.history)
        response = model.generate_content(prompt)
        return ChatResponse(response=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return FileResponse("chat.html")
