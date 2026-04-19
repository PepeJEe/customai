import httpx
from config import MODEL_NAME, SYSTEM_PROMPT, OLLAMA_URL
from logger import logger

async def receive_request(messages):
    try:
        logger.info("Sending request to Ollama")
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
            logger.info("Got response from Ollama: {content[:50]}")

        return result["message"]["content"]
    
    except Exception:
        logger.info("Failed to get response from Ollama")
        raise