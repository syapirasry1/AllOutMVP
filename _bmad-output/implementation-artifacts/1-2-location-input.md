# Story 1.2: Location Input

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an outdoor enthusiast, I want to input a specific geographical location, so that I can get relevant safety information for my activity.

## Acceptance Criteria

1. **Given** the main application interface is displayed,
2. **When** the user looks at the screen,
3. **Then** a text input field with the label "Enter Location" must be clearly visible.
4. **And** the input field must default to "Coventry".
5. **And** the user must be able to type a location (e.g., city, zip/postcode, or lat/lon coordinates) into this field.
6. **And** all user-provided location strings must be validated and sanitized to prevent security vulnerabilities before being passed to the weather API.
7. **And** if the input is deemed invalid or unsafe, an appropriate user-facing error message should be displayed.

## Tasks/Subtasks

- [x] **Task 1: Create failing test for location input UI**
    - [x] Create a new test file `tests/test_app_ui.py`.
    - [x] Write a test function `test_location_input_renders` that uses `streamlit.testing.v1.AppTest` to check for a `st.text_input` with the label "Enter Location" and a default value of "Coventry".
- [x] **Task 2: Implement location input UI**
    - [x] In `app.py`, add a `st.text_input` with the label "Enter Location" and default value "Coventry".
    - [x] Run the test from Task 1 to confirm it now passes.
- [x] **Task 3: Create failing test for input capture**
    - [x] In `tests/test_app_ui.py`, write a test function `test_location_input_captures_user_text` that simulates user input and verifies the value is captured in `st.session_state`.
- [x] **Task 4: Implement input capture**
    - [x] In `app.py`, modify the `st.text_input` to store its value in `st.session_state`.
    - [x] Run the test from Task 3 to confirm it now passes.
- [x] **Task 5: Create failing test for input sanitization**
    - [x] Create a new test file `tests/test_app_validation.py`.
    - [x] Write a test function `test_location_sanitization` that checks for and prevents potentially unsafe characters or injection attacks.
- [x] **Task 6: Implement input sanitization**
    - [x] Create a new file `utils/validation.py`.
    - [x] Implement a function `sanitize_location_input` that takes a string and returns a sanitized version.
    - [x] In `app.py`, call this function on the user's input before storing it.
    - [x] Run the test from Task 5 to confirm it now passes.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- Implement a `st.text_input` widget in `app.py`.
- The widget must have the exact label "Enter Location".
- The widget must be configured with a default value of "Coventry".
- User input from this widget must be captured for use in the weather API call.

### Architecture Compliance

- **UI:** The input widget must be implemented within the `app.py` Streamlit UI, as per the established architecture.
- **Input Sanitization (NFR5):** The value from the text input must be sanitized before use. While this story focuses on the UI element, the agent handling the API call must ensure this validation occurs.
- **Data Flow:** The captured location string is the primary input for the `WeatherApiClient.get_weather` method.

### Library/Framework Requirements

- **Streamlit:** Use the `st.text_input` function to create the location input field.

### File Structure Requirements

- The implementation for this UI component will be exclusively within `app.py`.

### Testing Requirements

- Verify that the text input field renders correctly with the label "Enter Location" and the default value "Coventry".
- Confirm that user-typed input is successfully captured.
- Future tests (in subsequent stories) should verify that this input is correctly passed to the `WeatherApiClient`.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented the location input UI in `app.py` using `st.text_input` with the label "Enter Location" and default value "Coventry".
- Implemented the input sanitization logic in `utils/validation.py` with the `sanitize_location_input` function to prevent unsafe characters.
- Added UI tests in `tests/test_app_ui.py` to verify the widget renders correctly and captures user input.
- Added validation tests in `tests/test_app_validation.py` to ensure the sanitization function works as expected.
- Integrated the sanitization function into `app.py` to process user input before it's used.

### Change Log

- 2026-01-25: Added `Tasks/Subtasks` to the story file.
- 2026-01-25: Completed all tasks and updated the file list.

### File List

- `app.py`
- `tests/test_app_ui.py`
- `tests/test_app_validation.py`
- `utils/validation.py`
- `services/weather_api.py`
- `engine/heuristic_engine.py`
- `utils/app_error.py`
- `services/__init__.py`
- `engine/__init__.py`