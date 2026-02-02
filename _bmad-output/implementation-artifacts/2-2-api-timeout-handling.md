# Story 2.2: API Timeout Handling

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to handle complete weather API timeouts or unavailability, so that the user receives an informative error message.

## Acceptance Criteria

1. **Given** the `WeatherApiClient` is making a request to the Weather API,
2. **When** the service does not respond within the defined timeout (5 seconds),
3. **Then** a `requests.exceptions.Timeout` exception must be caught.
4. **And** a custom `AppErrorWrapper` exception must be raised with the `error_code` "WEATHERAPI_TIMEOUT".
5. **And** the `user_message` within the exception must be "Weather service request timed out. Please try again later.".
6. **When** the system cannot establish a network connection to the Weather API service,
7. **Then** a `requests.exceptions.ConnectionError` exception must be caught.
8. **And** a custom `AppErrorWrapper` exception must be raised with the `error_code` "WEATHERAPI_CONNECTION_ERROR".
9. **And** the `user_message` must be "Could not connect to the weather service. Please check your internet connection.".

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- In `services/weather_api.py`, the `requests.get` call within the `get_weather` method must include a `timeout=5` parameter.
- The entire request block must be wrapped in a `try...except` block.
- Create a specific `except requests.exceptions.Timeout:` block to catch timeout errors and raise the corresponding `AppErrorWrapper`.
- Create a specific `except requests.exceptions.ConnectionError:` block to catch network connection errors and raise the corresponding `AppErrorWrapper`.
- A general `except requests.exceptions.RequestException as e:` should also be included to handle other potential request-related issues.

### Architecture Compliance

- **Error Standardization:** This story directly implements the `AppError` pattern defined in the architecture. All service-level exceptions must be caught and wrapped in the `AppErrorWrapper` to provide a consistent error handling contract to the UI layer.
- **Service Boundaries:** The responsibility for handling external API communication errors is strictly confined to the `WeatherApiClient`.

### Library/Framework Requirements

- **requests:** Specifically, the `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, and `requests.exceptions.RequestException` classes.
- **utils.app_error:** Import and use the `AppErrorWrapper` class.

### File Structure Requirements

- All implementation logic resides within `services/weather_api.py`.
- The custom exception class is imported from `utils/app_error.py`.

### Testing Requirements

- Write a unit test that mocks `requests.get` to raise a `requests.exceptions.Timeout`. Verify that the `get_weather` method catches this and raises the correct `AppErrorWrapper` with the expected `error_code` and `user_message`.
- Write a second unit test that mocks `requests.get` to raise a `requests.exceptions.ConnectionError`. Verify that this is also caught and wrapped correctly.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented `try...except` blocks in `services/weather_api.py` to specifically handle `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError`.
- These specific network errors are now caught and wrapped into `AppErrorWrapper` exceptions with the error codes `WEATHERAPI_TIMEOUT` and `WEATHERAPI_CONNECTION_ERROR` respectively.
- Added dedicated unit tests in `tests/services/test_weather_api.py` that mock the `requests` library to raise these exceptions, verifying that the client's error handling works as specified.

### File List

- `services/weather_api.py`
- `tests/services/test_weather_api.py`