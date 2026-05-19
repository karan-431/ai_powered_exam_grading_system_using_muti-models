from utils.ollama_client import generate
import logging

logger = logging.getLogger(__name__)

async def build_marking_scheme(raw_answer_key: str) -> str:
    """
    Converts raw answer key text into a structured marking scheme using Llama3.
    """
    logger.info("Building structured marking scheme using llama3:latest")
    
    prompt = f"""You are an expert examiner. Your task is to convert the following raw answer key into a well-structured marking scheme.
    
Identify each question, the expected correct answer or key points, and the marks allocated per question (if any are specified).
    
IMPORTANT: Return the response as a clear, structured JSON strictly following this format:
[
  {{
    "question_number": "1",
    "expected_answer": "...",
    "allocated_marks": ...
  }}
]

Do not include markdown code block formatting (like ```json) in your final output, just raw JSON.

Raw Answer Key:
{raw_answer_key}
"""

    try:
        response = await generate(
            model="llama3:latest",
            prompt=prompt
        )
        return response.strip()
    except Exception as e:
        logger.error(f"Scheme building failed: {e}")
        raise
