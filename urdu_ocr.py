from PIL import Image
import pytesseract

# Path to the Tesseract executable (change this path if needed)
# On Windows, it might look something like this:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Linux or MacOS, you may not need to change it if it's already in the PATH.

# Set the path to your Tesseract installation (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# OCR function for reading Urdu text
def extract_urdu_text(image_path):
    try:
        # Open the image using Pillow
        img = Image.open(image_path)

        # Perform OCR on the image, specifying the Urdu language
        text = pytesseract.image_to_string(img, lang='urd')  # 'udm' for Urdu language

        # Return the extracted text
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    # Path to your image containing Urdu text
    image_path = "images/sample.PNG"  # Change this to your image file path

    extracted_text = extract_urdu_text(image_path)
    
    if extracted_text:
        print("Extracted Urdu Text:")
        print(extracted_text)
    else:
        print("No text extracted from the image.")
