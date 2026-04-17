import httpx
from config import MODEL_NAME, SYSTEM_PROMPT, OLLAMA_URL
async def receive_request(messages):
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": full_messages,
                "stream": False
            }
            )

        result = response.json()
        return result["message"]["content"]