from utils.ollama_client import generate
import logging

logger = logging.getLogger(__name__)

async def evaluate_answers(student_answers: str, marking_scheme: str) -> str:
    """
    Evaluates student answers against the marking scheme using Llama3.
    """
    logger.info("Evaluating student answers using llama3:latest")
    
    prompt = f"""You are an expert examiner grading a student's answer sheet. Evaluate the student's answers against the marking scheme.

Be fair but precise. If a student's answer captures the essence of the expected answer, award full marks for that question. If it is partially correct, award partial marks. If it is completely wrong or missing, award 0.

At the very end of your evaluation, you MUST provide a final total score in the exact JSON format below. Do not wrap this JSON block in markdown backticks:

{{
  "total_obtained": <total_marks_awarded>,
  "total_possible": <total_marks_available>
}}

Marking Scheme:
{marking_scheme}

Student's Extracted Answers:
{student_answers}

Provide your detailed question-by-question evaluation followed by the final JSON block:
"""

    try:
        response = await generate(
            model="llama3:latest",
            prompt=prompt
        )
        return response
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise
