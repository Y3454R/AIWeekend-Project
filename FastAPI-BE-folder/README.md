## To run the application 
```
pip install fastapi uvicorn python-dotenv httpx
uvicorn main:app --reload
```
As a modification use the following
Implement True Chat History: Modify the /chat endpoint to manage a conversation. If a user asks a follow-up question like, "What if the total flow in the system?", the backend should combine this with the previous parameters to form a new, complete query for the AI
