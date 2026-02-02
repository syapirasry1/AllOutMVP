# Story 4.1: LLM-Powered Conversational Explanation

Status: **DONE** (v3.7.0 - Enhanced)

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to generate a conversational explanation of the safety status using an LLM, so that users understand the "so what" of the weather data.

## Acceptance Criteria

1.  **Given** a `GeminiInput` object (containing `HeuristicOutput` and raw weather data),
2.  **When** a new `GeminiLLMClient`'s `get_explanation` method is called,
3.  **Then** a prompt must be constructed that instructs the LLM to provide a concise, conversational explanation that **strictly aligns** with the heuristic decision and **never contradicts it**.
4.  **And** the system must make a call to the configured Gemini model (`gemini-2.5-flash`) using the `google-generativeai` library.
5.  **And** the LLM's response text must be successfully parsed into a `GeminiOutput` Pydantic model.
6.  **And** all potential Gemini API errors (e.g., API error, prompt blocked, response blocked, empty response) must be caught and re-raised as a custom `AppErrorWrapper` with a specific `error_code` (e.g., `GEMINI_API_ERROR`).
7.  **And** if the `GEMINI_API_KEY` is not found in the environment, an `AppErrorWrapper` with code `GEMINI_API_KEY_MISSING` must be raised on initialization.
8.  **Given** the Gemini API request times out (exceeds 6.0 seconds),
9.  **When** `get_explanation` is called,
10. **Then** an `AppErrorWrapper` with error_code "GEMINI_TIMEOUT" must be raised.
11. **And** the `user_message` must be "Request timed out. Please try again."
    

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- Create a new file: `services/gemini_llm.py`.
- Inside this file, create a `GeminiLLMClient` class.
- The `__init__` method must configure the `google-generativeai` library with the `GEMINI_API_KEY` from the environment, raising an `AppErrorWrapper` if it's missing.
- The client must be configured to use the `gemini-2.5-flash` model, as specified in the project architecture.
- Create a `get_explanation` method with the following signature:
      `def get_explanation(self, input_data: GeminiInput) -> GeminiOutput:`
- The `GeminiInput` object is a Pydantic model defined in `services/models.py` with the following structure:
  ```python
  class CurrentWeatherForGemini(BaseModel):
      temp_c: float
      feelslike_c: float
      wind_mph: float
      precip_mm: float
      uv: float

  class DayForecastForGemini(BaseModel):
      daily_chance_of_rain: int

  class GeminiInput(BaseModel):
      location_name: str
      current_weather: CurrentWeatherForGemini
      day_forecast: DayForecastForGemini
      heuristic_output: HeuristicOutput
  ```
- The `get_explanation` method will extract `location_name`, `current_weather`, `day_forecast`, and `heuristic_output` from this `GeminiInput` object for prompt construction.
- Implement robust prompt engineering within `get_explanation` to ensure the LLM's response is concise (under 250 words), conversational, and strictly adheres to the logic of the heuristic decision.
- After receiving the raw text response from the Gemini API, the `get_explanation` method must parse this text into a `GeminiOutput` Pydantic model. This model will automatically apply validation, including the word count check.
- The `get_explanation` method must return a `GeminiOutput` Pydantic model, defined in `services/models.py` with a validator to enforce the word count:
  ```python
  class GeminiOutput(BaseModel):
      explanation: str

      @validator('explanation')
      def word_count_must_be_under_250(cls, v):
          word_count = len(v.split())
          if word_count > 250:
              raise ValueError(f"Explanation exceeds 250 words (count: {word_count})")
          return v
  ```

#### Prompt Structure

The prompt constructed for the LLM must be a clear, concise instruction that includes the following information from the `GeminiInput` object:

1.  **System Instruction:** Clearly state the role of the LLM (e.g., "You are an AI assistant providing safety explanations for outdoor activities. Your response must strictly align with the provided safety decision and never contradict it.").
2.  **User's Query Context:**
    *   Location: `GeminiInput.location_name`
    *   Date: (Not directly provided in `GeminiInput` but can be passed or inferred if needed for prompt). For now, focus on the available fields.
3.  **Heuristic Output Details:**
    *   Decision: `GeminiInput.heuristic_output.decision`
    *   Weighted Score: `GeminiInput.heuristic_output.weighted_score`
    *   Notes: `GeminiInput.heuristic_output.notes`
    *   Hard-Stop Reasons: `GeminiInput.heuristic_output.hard_stop_reasons` (if any)
4.  **Raw Weather Data:**
    *   Current Temperature (feels like): `GeminiInput.current_weather.feelslike_c`
    *   Wind Speed: `GeminiInput.current_weather.wind_mph`
    *   Precipitation: `GeminiInput.current_weather.precip_mm`
    *   UV Index: `GeminiInput.current_weather.uv`
    *   Chance of Rain (today): `GeminiInput.day_forecast.daily_chance_of_rain`
5.  **Output Constraints:**
    *   Concise: Under 250 words.
    *   Conversational tone.
    *   Focus on the "so what" for outdoor enthusiasts.
    *   If decision is "GO", justify and provide general safety reminders.
    *   If decision is "MAYBE" or "NO-GO", clearly highlight key risks and reasons.

- Use a `try...except` block to handle potential exceptions from the `generate_content` call and wrap them in the appropriate `AppErrorWrapper`.

#### Error Handling Mapping

The `get_explanation` method must check for and handle the following conditions, raising an `AppErrorWrapper` with the specified `error_code`:

| Condition                                            | Implementation Check                                                                                               | `error_code`                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| API Key is missing.                                  | `os.getenv("GEMINI_API_KEY")` is `None` on initialization.                                                         | `GEMINI_API_KEY_MISSING`      |
| The user's prompt was blocked by safety filters.     | After the API call, check if `response.prompt_feedback.block_reason` exists.                                       | `GEMINI_PROMPT_BLOCKED`       |
| The model's generated response was blocked.          | After the API call, check if any `candidate.finish_reason` in the response is `'SAFETY'`.                          | `GEMINI_RESPONSE_BLOCKED`     |
| The API call returns successfully but with no text.  | After the API call, check if `response.text` is `None` or an empty string.                                         | `GEMINI_EMPTY_RESPONSE`       |
| A general API error occurs during the call.          | Catch a general `google.api_core.exceptions.GoogleAPICallError` or a broad `Exception`.                            | `GEMINI_API_ERROR`            |
| An entirely unexpected error occurs.                 | Use a final, broad `except Exception:` block to catch any other unhandled exceptions.                              | `GEMINI_UNEXPECTED_ERROR`     |
| The Gemini API request times out (exceeds 6.0 seconds). | Catch `TimeoutError` (or a more specific timeout exception from the library, like `google.api_core.exceptions.DeadlineExceeded`). | `GEMINI_TIMEOUT`              |

**Implementation Example for Timeout:**
```python
try:
    # The google-generativeai library uses a request_options dictionary
    # to pass configuration like timeouts to the underlying transport layer.
    model = genai.GenerativeModel(
        'gemini-2.5-flash'
    )
    response = model.generate_content(
        prompt,
        request_options={'timeout': 6.0}
    )
# The specific exception for timeouts might be library-dependent.
# A general TimeoutError or a specific one like DeadlineExceeded should be caught.
except (TimeoutError, google.api_core.exceptions.DeadlineExceeded):
    raise AppErrorWrapper(
        error_code="GEMINI_TIMEOUT",
        user_message="Request timed out. Please try again."
    )
```

### Architecture Compliance

- **Service Layer:** This client must be implemented in the `services/` layer, encapsulating all interaction with the external Gemini LLM service. The `GeminiLLMClient` consumes processed data from other services (e.g., weather data, heuristic output) to provide its explanation.
- **Error Standardization:** All exceptions originating from the `google-generativeai` library must be caught and wrapped in the standard `AppErrorWrapper` to ensure consistent error handling upstream in `app.py`.
- Data Flow: The client will receive the `GeminiInput` Pydantic model and return a validated `GeminiOutput` model. The `explanation` attribute from this model will be displayed in the Streamlit UI.

### Library/Framework Requirements

- **google-generativeai:** Use this library to interact with the Gemini API.
- **python-dotenv:** Use to load the `GEMINI_API_KEY` from the `.env` file.
- **utils.app_error:** Import and use the `AppErrorWrapper` for error handling.

### File Structure Requirements

- The primary implementation will be in `services/gemini_llm.py`.
- The `GeminiInput` model (and its nested components) is explicitly defined in `services/models.py`.

### Testing Requirements

- **Initialization Test:**
    - Write a unit test for the `__init__` method to verify it raises an `AppErrorWrapper` with `GEMINI_API_KEY_MISSING` when the API key environment variable is not set.

- **Prompt Construction Tests:**
    - Write unit tests for the `get_explanation` method that mock the `generate_content` call.
    - Verify that the prompt sent to the mock function is correctly constructed based on `GeminiInput` data for:
        - A "GO" decision.
        - A "MAYBE" decision.
        - A "NO-GO" decision.
    - Ensure all required context (location, weather details, heuristic output) is present in the constructed prompt.

- **Response Validation Tests:**
    - Verify that a raw string response from the mocked Gemini API call (representing a valid explanation) is successfully used to instantiate and validate a `GeminiOutput` object.
    - Verify that a raw string response from the mocked Gemini API call that exceeds 250 words raises a `pydantic.ValidationError`.

- **Error Handling Tests:**
    - Write unit tests that mock the `google-generativeai` library to simulate each error condition specified in the "Error Handling Mapping" section.
    - For each simulated error, verify that the `get_explanation` method catches the underlying condition and correctly raises an `AppErrorWrapper` with the precise `error_code` (e.g., `GEMINI_PROMPT_BLOCKED`, `GEMINI_EMPTY_RESPONSE`, `GEMINI_API_ERROR`).
    - Write a unit test that mocks the `google-generativeai` library to raise a `google.api_core.exceptions.DeadlineExceeded` (or similar timeout exception). Verify that `get_explanation` correctly raises an `AppErrorWrapper` with `GEMINI_TIMEOUT` and the specified `user_message`.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented the `GeminiLLMClient` in `services/gemini_llm.py` to encapsulate all interactions with the Google Gemini API.
- The client's `__init__` method checks for the `GEMINI_API_KEY` and raises a `GEMINI_API_KEY_MISSING` error if it's not found.
- The `get_explanation` method constructs a detailed prompt using weather, forecast, and heuristic data from a `GeminiInput` object.
- Implemented comprehensive error handling to catch and wrap all potential API issues (e.g., `PROMPT_BLOCKED`, `RESPONSE_BLOCKED`, `TIMEOUT`, `API_ERROR`) into standardized `AppErrorWrapper` exceptions.
- Added a custom `@field_validator` to the `GeminiOutput` model in `services/models.py` to ensure the explanation does not exceed 250 words.
- Developed a full suite of unit tests in `tests/services/test_gemini_llm.py` using `unittest.mock` to validate prompt construction, response parsing, and every error handling path without making real API calls.

### File List
- `services/gemini_llm.py`
- `services/models.py`
- `tests/services/test_gemini_llm.py`