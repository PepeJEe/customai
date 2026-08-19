from fastapi import FastAPI
from pydantic import BaseModel
from config import (
    MODEL_NAME,
    DEFAULT_HOSTNAME,
    DEFAULT_PORT,
)
from llm import receive_request
from logger import logger
import uvicorn

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list
    model: str = MODEL_NAME

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received: {request.messages[-1]["content"]}")
        response = await receive_request(request.messages)
        logger.info(f"Response: {response[:50]}")
        return {
            "choices": [
                {
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop"
            }
        ]  
    }
    except Exception:
        logger.exception("Failed to process request")
        raise

if __name__ == '__main__':
    config = uvicorn.Config(
        app,
        host=DEFAULT_HOSTNAME,
        port=DEFAULT_PORT,
    )
    server = uvicorn.Server(config)
    try:
        server.run()
    except KeyboardInterrupt:
        pass
