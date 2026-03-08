import easyocr
import io
import re
from PIL import Image

# Loaded once when the module is first imported — avoids reloading the model on every request
_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


def extract_text(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    reader = _get_reader()

    # EasyOCR returns [(bounding_box, text, confidence), ...]
    raw = reader.readtext(img, detail=1)

    # Join all text fragments with confidence > 30% in reading order
    all_text = " ".join(text for _, text, conf in raw if conf > 0.3)

    return _extract_ingredients_section(all_text)


def _extract_ingredients_section(text):
    # Look for "ingredients:" or "ingredient:" header (case insensitive)
    match = re.search(r'ingredients?\s*:?\s*(.+)', text, re.IGNORECASE | re.DOTALL)
    if match:
        section = match.group(1)
        # Cut off at common non-ingredient sections
        stop = re.search(
            r'(contains|allergen|nutrition|serving|storage|keep|best before|manufactured|distributed)',
            section, re.IGNORECASE
        )
        if stop:
            section = section[:stop.start()]
    else:
        # No "ingredients:" header found — treat all detected text as ingredients
        section = text

    # Format as clean comma-separated list
    return ", ".join(
        part.strip()
        for part in re.split(r'[,\n;]', section)
        if part.strip() and len(part.strip()) > 1
    )
