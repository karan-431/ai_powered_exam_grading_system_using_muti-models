import re
import json
import logging
from agents.extractor import extract_handwritten_text
from agents.scheme_builder import build_marking_scheme
from agents.evaluator import evaluate_answers
from agents.validator import validate_confidence

logger = logging.getLogger(__name__)

async def unload_model(model_name: str):
    """Unloads a model from Ollama VRAM to free up space."""
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            await client.post("http://localhost:11434/api/generate", json={"model": model_name, "keep_alive": 0})
        logger.info(f"Successfully unloaded {model_name} from memory")
    except Exception as e:
        logger.warning(f"Failed to unload {model_name}: {e}")

async def run_pipeline(image_paths: list[str], raw_answer_key: str, max_marks: float) -> dict:
    """
    Orchestrates the AI exam grading pipeline.
    """
    try:
        # Free up memory before running heavy vision model
        await unload_model("llama3:latest")
        
        # Step 1: Extract text from answer sheet images
        student_answers = await extract_handwritten_text(image_paths)
        if not student_answers:
            raise ValueError("Failed to extract text from images.")

        # Free up memory before running heavy text model reasoning
        await unload_model("qwen2.5vl:3b")
        
        # Step 2: Build marking scheme
        marking_scheme = await build_marking_scheme(raw_answer_key)

        # Step 3: Evaluate answers
        evaluation = await evaluate_answers(student_answers, marking_scheme)

        # Step 4: Validate confidence
        confidence = await validate_confidence(evaluation)

        # Step 5: Extract marks
        obtained, possible = extract_marks(evaluation)
        
        # Step 6: Scale marks
        final_score = (obtained / possible) * max_marks if possible > 0 else 0.0

        return {
            "student_answers": student_answers,
            "marking_scheme": marking_scheme,
            "evaluation": evaluation,
            "confidence": confidence,
            "obtained": obtained,
            "possible": possible,
            "final_score": round(final_score, 2)
        }

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise e

def extract_marks(evaluation: str) -> tuple[float, float]:
    """
    Tries to extract 'total_obtained' and 'total_possible' from the evaluation text.
    First tries JSON parsing, then regex fallback.
    """
    # 1. Try to find JSON block
    # Often models wrap JSON in markdown block or just output it at the end
    json_match = re.search(r'\{[^{}]*"total_obtained"\s*:\s*([\d.]+)[^{}]*"total_possible"\s*:\s*([\d.]+)[^{}]*\}', evaluation, re.IGNORECASE)
    
    if json_match:
        try:
            return float(json_match.group(1)), float(json_match.group(2))
        except ValueError:
            pass

    # 2. Fallback text regex
    text_match = re.search(r'Total:\s*([\d.]+)\s*/\s*([\d.]+)', evaluation, re.IGNORECASE)
    if text_match:
        return float(text_match.group(1)), float(text_match.group(2))

    # 3. Wider regex fallback
    wide_match = re.search(r'total_obtained[^\d]*([\d.]+).*total_possible[^\d]*([\d.]+)', evaluation, re.IGNORECASE | re.DOTALL)
    if wide_match:
        return float(wide_match.group(1)), float(wide_match.group(2))

    logger.warning("Could not extract marks cleanly. Returning 0/1.")
    return 0.0, 1.0 # Prevent division by zero later
