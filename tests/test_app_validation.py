from utils.validation import sanitize_location_input

def test_location_sanitization():
    """
    Test that the location input is sanitized correctly.
    """
    unsafe_input = "<script>alert('xss')</script>"
    sanitized_input = sanitize_location_input(unsafe_input)
    assert "<" not in sanitized_input
    assert ">" not in sanitized_input
