import asyncio

import httpx
from config import MODEL_NAME, SYSTEM_PROMPT, OLLAMA_URL
async def receive_request(messages):
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        for attempt in range(3):
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "message": full_messages,
                    "stream": False
                }
            )

            result = response.json()
            if "message" not in result:
                return f"Error from Ollama: {result}"
            print(result)
            content = result["message"]["content"]

            if content:
                return content

            await asyncio.sleep(2)
    return "Sorry I am still loading, please try again!"