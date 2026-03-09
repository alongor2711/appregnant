"""
Mock heavy dependencies before any app module is imported.
This lets CI run tests without installing easyocr + PyTorch (~1GB).
"""
import sys
from unittest.mock import MagicMock

# Stub out easyocr so `import easyocr` in ocr.py doesn't fail
sys.modules["easyocr"] = MagicMock()
