# Story 1.6: Loading Feedback

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an outdoor enthusiast, I want to see a loading indicator when the system is processing my request, so that I know the application is working.

## Acceptance Criteria

1. **Given** a user has entered a location and date,
2. **When** they click the "Assess Safety" button,
3. **Then** a spinner or similar loading indicator must be displayed with the message "Fetching weather data and assessing conditions...".
4. **And** this loading indicator must wrap the entire assessment process (API calls, engine execution).
5. **And** the loading indicator must disappear automatically once the final assessment results are displayed.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- In `app.py`, use a `with st.spinner(...)` block to wrap the code that executes after the "Assess Safety" button is clicked.
- The spinner must display the exact text: "Fetching weather data and assessing conditions...".
- The block should encompass the instantiation and use of `WeatherApiClient`, `HeuristicSafetyEngine`, and the subsequent rendering of results.

### Architecture Compliance

- **UI:** This feedback mechanism must be implemented within `app.py` as a direct response to user interaction, consistent with the architecture's focus on a responsive UI.
- **Process Patterns:** This directly implements the "Loading States (Feedback)" process pattern defined in the architecture, which mandates using `st.spinner` for long-running operations.

### Library/Framework Requirements

- **Streamlit:** Use the `st.spinner` context manager.

### File Structure Requirements

- The implementation for this UI behavior will be exclusively within `app.py`.

### Testing Requirements

- Manually verify that clicking the "Assess Safety" button immediately displays the spinner with the correct text.
- Verify that the spinner is removed from the UI once the results (either success or an error message) are rendered.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented the loading indicator in `app.py` by wrapping the main processing logic inside a `with st.spinner(...)` block.
- The spinner displays the required message: "Fetching weather data and assessing conditions...".
- This ensures the user receives immediate feedback after clicking the "Assess Safety" button, which persists until the final results are displayed.

### File List

- `app.py`