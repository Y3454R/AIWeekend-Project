from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Defines the structure for incoming chat requests."""
    question: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    """Defines the structure for outgoing chat responses."""
    answer: str