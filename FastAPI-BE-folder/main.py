from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Import components from utility files
from schemas import ChatRequest, ChatResponse
from prompt import SYSTEM_PROMPT
from gemini_client import call_gemini_api
from html_content import HTML_CONTENT

# Initialize the FastAPI application
app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a question, combines it with the system prompt,
    and gets an answer from the Gemini API.
    """
    # Construct the full prompt to send to the model
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser question: {request.question}"
    
    # Call the Gemini API and get the answer
    answer = await call_gemini_api(full_prompt)
    
    return ChatResponse(answer=answer)

@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    """
    Serves the simple HTML chat interface from the utility file.
    """
    return HTMLResponse(content=HTML_CONTENT)
