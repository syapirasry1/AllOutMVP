# Story 4.2: Low AI Response Latency

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an outdoor enthusiast, I want to receive the AI-powered safety explanation quickly, so that I can make timely decisions.

## Acceptance Criteria

1.  **Given** a valid request is sent to the Gemini LLM via the `GeminiLLMClient.get_explanation` method,
2.  **When** the LLM client receives the response,
3.  **Then** the time taken from sending the request to receiving the full explanation must be **under 6.5 seconds** (NFR1).

## Dev Notes
**DEV AGENT GUARDRAILS:**

This story represents a Non-Functional Requirement (NFR) that applies to the implementation of the `GeminiLLMClient`.

### Technical Requirements

- The implementation of the `get_explanation` method in `services/gemini_llm.py` must be optimized for performance.
- **Prompt Efficiency:** The prompt sent to the Gemini model should be engineered to be as concise as possible while still providing the necessary context, as shorter prompts generally lead to faster responses.
- **API Timeouts:** Configure the Gemini API request timeout to **6.0 seconds** in the `GeminiLLMClient.get_explanation()` method. This provides a 0.5-second buffer from the 6.5-second NFR1 requirement, ensuring the application halts and raises an error before the threshold is exceeded. If the request exceeds 6.0 seconds, an appropriate `AppErrorWrapper` must be raised (see Story 4.1 for `GEMINI_API_ERROR` handling details). Expected latency with `gemini-2.5-flash` is 2-3 seconds average, so a 6.0-second timeout provides a safety buffer for network delays.
- **Model Selection:** The choice of the `gemini-2.5-flash` model is suitable for this task, balancing capability and performance.

### Architecture Compliance

- **Performance (NFR1):** This story is the direct expression of NFR1. The `GeminiLLMClient` is the sole component responsible for meeting this latency requirement.
- **User Experience:** Adhering to this NFR is critical for a positive user experience, preventing users from abandoning the assessment due to long wait times.

### Library/Framework Requirements

- **google-generativeai:** The implementation must be mindful of any performance tuning options available within this library, such as setting client-side timeouts on requests.

### File Structure Requirements

- The performance considerations apply directly to the code within `services/gemini_llm.py`.

### Testing Requirements

- **Timeout Exception Handling Test:**
    - Write a unit test that mocks the `google-generativeai` library's `generate_content` call to raise a `TimeoutError` (or `google.api_core.exceptions.DeadlineExceeded`).
    - Verify that the `GeminiLLMClient.get_explanation` method catches this timeout exception and correctly raises an `AppErrorWrapper` with `error_code="GEMINI_TIMEOUT"` and the specified `user_message`.

- **Performance Measurement Test (NFR1):**
    - This is a critical non-functional test.
    - Implement a unit test that calls `GeminiLLMClient.get_explanation` with representative input data.
    - Measure the execution time of this call (e.g., using `time.time()`).
    - Assert that the measured latency is consistently **under 6.5 seconds**.
    - This test should ideally be run against the live Gemini API (or a high-fidelity mock that accurately simulates real-world latency) to get realistic measurements.
    - If latency consistently exceeds the 6.5-second threshold, the prompt engineering, model configuration, and client-side timeouts must be revisited and optimized.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created

### File List