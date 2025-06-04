from PIL import Image
import pytesseract
import cv2
import shutil

# ✅ Dynamic path setup
if not shutil.which("tesseract"):
    # If not found in system PATH, manually set it (Windows fallback)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_to_text(image_path:str)->str:
    image=cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found or unreadable: {image_path}")
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    text=pytesseract.image_to_string(gray)
    return text 

