from utils.ollama_client import generate
import base64
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

async def extract_handwritten_text(image_paths: list[str]) -> str:
    """
    Extracts handwritten text from a list of image paths using Qwen2.5-VL.
    """
    logger.info(f"Extracting text from {len(image_paths)} images using qwen2.5vl:3b")
    
    encoded_images = []
    for path in image_paths:
        try:
            with Image.open(path) as img:
                # Convert to RGB and resize if too large to save memory/tokens
                img = img.convert("RGB")
                img.thumbnail((768, 768))
                
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
                encoded_images.append(encoded)
        except Exception as e:
            logger.error(f"Error encoding image {path}: {e}")
            raise

    prompt = (
        "You are an expert OCR system. Extract all the handwritten text from the "
        "provided answer sheet images. Preserve the structure, especially the question "
        "numbers and answers. Return only the extracted text, nothing else."
    )
    
    try:
        response = await generate(
            model="qwen2.5vl:3b",
            prompt=prompt,
            images=encoded_images
        )
        return response
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
