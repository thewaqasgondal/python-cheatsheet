# OCR Examples

This directory contains Optical Character Recognition examples using Tesseract OCR.

## Prerequisites

Install Tesseract OCR:
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

For language support:
```bash
# Urdu language data
sudo apt-get install tesseract-ocr-urd  # Linux
brew install tesseract-lang  # macOS
```

## Files

### ocr_example.py
Basic OCR implementation for extracting text from images.

**Features:**
- Load images using PIL/Pillow
- Extract text from images using Tesseract
- Display extracted text

**Usage:**
```bash
python ocr_example.py
```

**Configuration:**
Update the Tesseract path:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

### urdu_ocr.py
Multi-language OCR support for Urdu text extraction.

**Features:**
- Urdu language text recognition
- Unicode text handling
- Image preprocessing for better accuracy

**Usage:**
```bash
python urdu_ocr.py
```

**Language Code:** `urd` for Urdu

---

### table_ext.py
Extract and parse tabular data from images.

**Features:**
- Table detection in images
- Text extraction from table cells
- Parsing structured data
- Export to pandas DataFrame

**Usage:**
```bash
python table_ext.py
```

## Tips for Better OCR Results

1. **Image Quality**
   - Use high-resolution images (300 DPI or higher)
   - Ensure good contrast
   - Remove noise and artifacts

2. **Preprocessing**
   - Convert to grayscale
   - Apply thresholding
   - Deskew images
   - Remove borders

3. **Text Detection**
   - Use appropriate language data
   - Configure PSM (Page Segmentation Mode)
   - Adjust OEM (OCR Engine Mode)

## Common Issues

- **Poor accuracy**: Improve image quality, try preprocessing
- **Language not supported**: Install required language data
- **Path errors**: Update Tesseract executable path
- **Unicode errors**: Ensure proper encoding for non-English text
