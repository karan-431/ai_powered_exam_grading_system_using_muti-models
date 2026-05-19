import httpx
import json
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate(model: str, prompt: str, images: list[str] = None) -> str:
    """
    Calls the local Ollama API to generate a response.
    
    Args:
        model: Make sure model is pulled via `ollama run <model>`
        prompt: The text prompt
        images: Optional list of base64 encoded strings
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    if images:
        payload["images"] = images

    # Timeout set to 300 seconds (5 minutes) as LLM inference can take time
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            logger.info(f"Sending prompt to Ollama ({model})...")
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error calling Ollama: {e}")
            raise Exception(f"Failed to communicate with Ollama: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Ollama: {e}")
            raise Exception("Invalid response format from Ollama.")
