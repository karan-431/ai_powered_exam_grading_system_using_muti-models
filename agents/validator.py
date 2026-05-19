from utils.ollama_client import generate
import logging

logger = logging.getLogger(__name__)

async def validate_confidence(evaluation: str) -> str:
    """
    Validates the confidence of the evaluation using Llama3.
    Returns High, Medium, or Low.
    """
    logger.info("Validating evaluation confidence using llama3:latest")
    
    prompt = f"""You are a quality assurance AI. Review the following AI-generated evaluation of a student's exam.
    
Assess the quality and reasoning of the evaluation. Is it confident, clear, and logical? Are the assigned marks well-reasoned?

Your ONLY output should be one of these three exact words: High, Medium, or Low.
Do not provide any explanation or other text.

Evaluation:
{evaluation}
"""

    try:
        response = await generate(
            model="llama3:latest",
            prompt=prompt
        )
        # Clean up output
        confidence = response.strip().strip('.').capitalize()
        if confidence not in ["High", "Medium", "Low"]:
            confidence = "Medium" # Fallback
        return confidence
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return "Low" # Safe fallback
