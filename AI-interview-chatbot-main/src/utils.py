# src/utils.py

import re
import string
import logging
from datetime import datetime

# --- Text Cleaning Utilities ---

def clean_text(text):
    """
    Clean and standardize input text: lowercase, remove special characters, extra spaces.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def anonymize_text(text):
    """
    Anonymize sensitive info (basic): emails, phone numbers.
    """
    if not isinstance(text, str):
        return ""
    # Mask emails
    text = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', '[email]', text)
    # Mask phone numbers (simple patterns)
    text = re.sub(r'\b\d{10,}\b', '[phone]', text)
    text = re.sub(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[phone]', text)
    return text

# --- Logging Utility ---

def setup_logger(name="chatbot_logger", log_file="logs/chatbot.log", level=logging.INFO):
    """
    Set up a logger for the chatbot.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(fh)
    return logger

# --- Time Utility ---

def get_timestamp():
    """
    Return current timestamp as ISO string.
    """
    return datetime.now().isoformat()

# --- Example Usage ---

if __name__ == "__main__":
    raw = "  Hello, my email is john.doe@example.com and my phone is 123-456-7890!  "
    print("Cleaned:", clean_text(raw))
    print("Anonymized:", anonymize_text(raw))
    logger = setup_logger()
    logger.info("This is a test log entry.")
    print("Timestamp:", get_timestamp())
