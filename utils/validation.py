import re

def sanitize_location_input(location: str) -> str:
    """
    Sanitizes the location input by removing potentially unsafe characters.
    """
    if not isinstance(location, str):
        return ""
    # Remove characters that are not letters, numbers, spaces, commas, or hyphens
    sanitized = re.sub(r"[^a-zA-Z0-9\s,-]", "", location)
    return sanitized.strip()
