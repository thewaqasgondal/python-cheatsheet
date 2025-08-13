from PIL import Image
import pytesseract

# 1. Specify the path to the Tesseract executable
# For Windows users, set the path to your tesseract.exe
# Example: pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# On MacOS/Linux, Tesseract is generally installed in the system path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Modify as needed

# 2. Load the image from file
image_path = 'images/a.png'  # Change to your image file path
img = Image.open(image_path)

# 3. Apply OCR to extract text
extracted_text = pytesseract.image_to_string(img)

# 4. Output the extracted text
print("Extracted Text from Image:")
print(extracted_text)

# 5. (Optional) Save the image as a temporary file with text overlay
# img.show()  # Uncomment to display the image (optional)

