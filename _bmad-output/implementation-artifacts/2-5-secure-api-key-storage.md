# Story 2.5: Secure API Key Storage

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to store API keys securely, so that sensitive credentials are not exposed.

## Acceptance Criteria

1. **Given** the application is running,
2. **When** the `WeatherApiClient` is initialized,
3. **Then** it must load the API key from an environment variable named `WEATHERAPI_KEY`.
4. **And** the `python-dotenv` library must be used to load variables from a `.env` file.
5. **Given** the `WEATHERAPI_KEY` is not found in the environment,
6. **When** the `WeatherApiClient` is initialized,
7. **Then** an `AppErrorWrapper` with error code `WEATHERAPI_KEY_MISSING` must be raised.
8. **Given** any source code file in the project,
9. **Then** no file shall contain a hard-coded API key.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- In the `__init__` method of the `WeatherApiClient` class (`services/weather_api.py`), call `load_dotenv()` to load environment variables from a `.env` file.
- Use `os.getenv("WEATHERAPI_KEY")` to retrieve the API key.
- Implement a check to verify if the key was successfully loaded. If the key is `None` or an empty string, raise an `AppErrorWrapper` with `error_code="WEATHERAPI_KEY_MISSING"` and a descriptive `user_message`.

### Architecture Compliance

- **Security (NFR4):** This story is the direct implementation of NFR4, which mandates secure API key storage and prohibits hard-coding credentials.
- **Error Standardization:** Raising an `AppErrorWrapper` for a missing key aligns with the project's standardized error handling pattern.

### Library/Framework Requirements

- **python-dotenv:** Use the `load_dotenv` function to manage environment variables from a file.
- **os:** Use the `os` module to get environment variables.

### File Structure Requirements

- The implementation logic belongs in the `__init__` method of the `WeatherApiClient` in `services/weather_api.py`.
- The system depends on a `.env` file (created from `.env.example`) being present in the project root.

### Testing Requirements

- Write a unit test where the `WEATHERAPI_KEY` environment variable is deliberately unset.
- Verify that initializing the `WeatherApiClient` in this state raises an `AppErrorWrapper` with the `error_code` "WEATHERAPI_KEY_MISSING".
- Write a second test where the key is present, and verify that no exception is raised and the `api_key` attribute is set correctly.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- The `__init__` method of `WeatherApiClient` in `services/weather_api.py` now uses `os.getenv("WEATHERAPI_KEY")` to load the API key.
- A check was implemented to ensure that if the key is not found, an `AppErrorWrapper` with the error code `WEATHERAPI_KEY_MISSING` is raised.
- The `python-dotenv` library is used project-wide to load environment variables from the `.env` file.
- A dedicated unit test, `test_weather_api_key_missing_error`, was created in `tests/services/test_weather_api.py` to verify this specific error handling path, confirming the implementation is correct.

### File List

- `services/weather_api.py`
- `tests/services/test_weather_api.py`