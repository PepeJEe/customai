import httpx
from config import MODEL_NAME, SYSTEM_PROMPT, OLLAMA_URL
async def receive_request(messages):
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    async with httpx.AsyncClient(timeout=300.0) as client:
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
        return result["messages"]["content"]