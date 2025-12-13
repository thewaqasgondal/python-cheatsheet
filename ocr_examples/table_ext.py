import pytesseract
from PIL import Image
import pandas as pd
import re

# Define the path to your Tesseract executable (adjust this path as needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows path example

# Load the image
image_path = 'images/table.png'  # Update with your image path
img = Image.open(image_path)

# Use Tesseract to extract text from the image
extracted_text = pytesseract.image_to_string(img)

# Print the raw extracted text (optional for debugging)
print("Extracted Text:\n", extracted_text)

# Step 3: Parsing the extracted text into a structured table
# Assume the text is in tabular format, separated by spaces or other delimiters.
# For example, splitting by line breaks and tabs/spaces

rows = extracted_text.split("\n")
data = []

# Debugging: Print the rows before processing to check if there are any issues with the structure
print("\nRows extracted:")
print(rows)

# Process the rows to split them into columns
for row in rows:
    # Skip empty rows and rows with only spaces
    if row.strip():
        # Split the row by multiple spaces (or tabs)
        columns = re.split(r'\s{2,}', row.strip())  # Split by two or more spaces
        if len(columns) > 1:  # Avoid rows with a single column or empty rows
            data.append(columns)

# Check if we have any valid data
if not data:
    print("No valid data extracted from the image.")
else:
    # Step 4: Create a DataFrame (assuming the first row is headers)
    if len(data) > 1:
        df = pd.DataFrame(data[1:], columns=data[0])
        # Step 5: Save to CSV or Excel
        df.to_csv('extracted_table.csv', index=False)
        df.to_excel('extracted_table.xlsx', index=False)
        print("Table extracted and saved to extracted_table.csv / extracted_table.xlsx.")
    else:
        print("Not enough data to form a table.")
