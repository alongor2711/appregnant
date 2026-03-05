import pytesseract
from PIL import Image
import io


def extract_text(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(img)
    # Collapse newlines into commas for ingredient parsing
    text = ", ".join(
        part.strip()
        for part in text.replace("\n", ",").split(",")
        if part.strip()
    )
    return text
