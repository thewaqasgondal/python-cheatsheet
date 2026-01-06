"""
Basic OCR (Optical Character Recognition) Example

This module demonstrates how to extract text from images using Tesseract OCR.
It shows basic OCR functionality with proper error handling and configuration.
"""

import os
from PIL import Image
import pytesseract


def setup_tesseract_path() -> str:
    """
    Set up the Tesseract executable path based on the operating system.

    Returns:
        str: Path to the Tesseract executable

    Raises:
        EnvironmentError: If Tesseract is not found or path cannot be determined
    """
    # Common Tesseract installation paths
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # Windows
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",  # Windows 32-bit
        "/usr/bin/tesseract",  # Linux
        "/usr/local/bin/tesseract",  # macOS/Homebrew
        "/opt/homebrew/bin/tesseract",  # macOS/Homebrew (Apple Silicon)
    ]

    # Check if tesseract is in PATH
    import shutil
    if shutil.which("tesseract"):
        pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")
        return pytesseract.pytesseract.tesseract_cmd

    # Check common installation paths
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return path

    raise EnvironmentError(
        "Tesseract not found. Please install Tesseract OCR:\n"
        "- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n"
        "- macOS: brew install tesseract\n"
        "- Linux: sudo apt-get install tesseract-ocr"
    )


def extract_text_from_image(image_path: str, lang: str = 'eng') -> str:
    """
    Extract text from an image file using OCR.

    Args:
        image_path: Path to the image file
        lang: Language code for OCR (default: 'eng' for English)

    Returns:
        str: Extracted text from the image

    Raises:
        FileNotFoundError: If the image file doesn't exist
        Exception: For other OCR-related errors
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    try:
        # Open the image
        img = Image.open(image_path)

        # Perform OCR
        extracted_text = pytesseract.image_to_string(img, lang=lang)

        return extracted_text.strip()

    except Exception as e:
        raise Exception(f"OCR failed for {image_path}: {str(e)}")


def get_image_info(image_path: str) -> dict:
    """
    Get basic information about an image.

    Args:
        image_path: Path to the image file

    Returns:
        dict: Image information including size, format, etc.
    """
    try:
        with Image.open(image_path) as img:
            return {
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'filename': os.path.basename(image_path)
            }
    except Exception as e:
        return {'error': str(e)}


def process_multiple_images(image_paths: list, lang: str = 'eng') -> dict:
    """
    Process multiple images and extract text from each.

    Args:
        image_paths: List of paths to image files
        lang: Language code for OCR

    Returns:
        dict: Mapping of image paths to extracted text or error messages
    """
    results = {}

    for image_path in image_paths:
        try:
            text = extract_text_from_image(image_path, lang)
            results[image_path] = {
                'success': True,
                'text': text,
                'info': get_image_info(image_path)
            }
        except Exception as e:
            results[image_path] = {
                'success': False,
                'error': str(e),
                'info': get_image_info(image_path)
            }

    return results


def main():
    """Main function demonstrating OCR functionality."""
    print("=== OCR Example ===\n")

    try:
        # Setup Tesseract
        tesseract_path = setup_tesseract_path()
        print(f"Tesseract path: {tesseract_path}\n")

    except EnvironmentError as e:
        print(f"Setup Error: {e}")
        return

    # Define image paths to process
    image_dir = '../images'  # Adjust path as needed
    possible_images = [
        os.path.join(image_dir, 'a.png'),
        os.path.join(image_dir, 'sample.png'),
        os.path.join(image_dir, 'test.jpg')
    ]

    # Find existing images
    existing_images = [img for img in possible_images if os.path.exists(img)]

    if not existing_images:
        print("No sample images found. Please add images to the 'images' directory.")
        print("Supported formats: PNG, JPG, JPEG, BMP, TIFF")
        return

    print(f"Found {len(existing_images)} image(s) to process:\n")

    # Process images
    results = process_multiple_images(existing_images)

    # Display results
    for image_path, result in results.items():
        print(f"Image: {os.path.basename(image_path)}")
        info = result.get('info', {})

        if info and 'size' in info:
            print(f"  Size: {info['size']}")
            print(f"  Format: {info.get('format', 'Unknown')}")

        if result['success']:
            text = result['text']
            if text:
                print(f"  Extracted Text: {text[:100]}{'...' if len(text) > 100 else ''}")
            else:
                print("  No text found in image")
        else:
            print(f"  Error: {result['error']}")

        print()


if __name__ == "__main__":
    main()

