import os
import logging
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

def pdf_to_images(pdf_path: str) -> list:
    """
    Converts a PDF file into a list of PIL Image objects using PyMuPDF.
    Requires 'pymupdf' to be installed.
    """
    try:
        logger.info(f"Converting PDF to images: {pdf_path}")
        doc = fitz.open(pdf_path)
        images = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # 2x zoom for better resolution readable by OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        logger.info(f"Converted {len(images)} pages successfully.")
        return images
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise Exception(f"Failed to process PDF file: {e}")

def save_images(images: list, output_dir: str, prefix: str = "page") -> list[str]:
    """Helper to save images to disk and return paths."""
    paths = []
    os.makedirs(output_dir, exist_ok=True)
    for i, img in enumerate(images):
        path = os.path.join(output_dir, f"{prefix}_{i+1}.jpg")
        img.save(path, "JPEG")
        paths.append(path)
    return paths
