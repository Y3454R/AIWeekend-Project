from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Import components from utility files
from schemas import ChatRequest, ChatResponse
#from prompt import SYSTEM_PROMPT
from system_prompt_alternative import SYSTEM_PROMPT
from gemini_client import call_gemini_api
from html_content import HTML_CONTENT

# Initialize the FastAPI application
app = FastAPI()


file_path = 'vug_contours_6c1f9898.csv'
try:
    with open(file_path, 'r') as f:
        vug_data_string = f.read()
except FileNotFoundError:
    vug_data_string = "Error: Vug data file not found."

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a question, combines it with the system prompt,
    and gets an answer from the Gemini API.
    """

    # 3. Inject the file data into the template to create the final system prompt
    final_system_prompt = SYSTEM_PROMPT.format(csv_data=vug_data_string)

    # 4. Construct the full prompt to send to the model
    full_prompt = f"{final_system_prompt}\n\nUser question: {request.question}"
    # Construct the full prompt to send to the model
    
    
    # Call the Gemini API and get the answer
    answer = await call_gemini_api(full_prompt)
    
    return ChatResponse(answer=answer)

@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    """
    Serves the simple HTML chat interface from the utility file.
    """
    return HTMLResponse(content=HTML_CONTENT)