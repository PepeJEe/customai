from fastapi import FastAPI
from pydantic import BaseModel
from config import MODEL_NAME
from llm import receive_request

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list
    model: str = MODEL_NAME

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    response = await receive_request(request.messages)
    return {
        "choices": [
            {
            "messages": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": "stop"
        } 
    ]  
}

