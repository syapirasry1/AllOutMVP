from streamlit.testing.v1 import AppTest

def test_location_input_renders():
    """
    Test that the location input widget renders correctly.
    """
    at = AppTest.from_file("app.py")
    at.run()
    text_input = at.text_input(key="location")
    assert text_input.label == "Enter Location"
    assert text_input.value == "Coventry"

def test_location_input_captures_user_text():
    """
    Test that user input from the location text input widget is captured.
    """
    at = AppTest.from_file("app.py")
    at.run()
    text_input = at.text_input(key="location")
    text_input.input("London").run()
    assert at.session_state["location"] == "London"
