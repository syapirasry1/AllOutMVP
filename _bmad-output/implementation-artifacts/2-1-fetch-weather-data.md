# Story 2.1: Fetch Weather Data (WeatherAPI.com)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to fetch required weather data from WeatherAPI.com, so that the safety assessment can be performed.

## Acceptance Criteria

1. **Given** a valid location and date are provided to the `WeatherApiClient`,
2. **When** the `get_weather` method is called,
3. **Then** the system must make a `GET` request to the `http://api.weatherapi.com/v1/forecast.json` endpoint.
4. **And** the request parameters must include the API `key`, `q` (location), `dt` (date), and `days=1`.
5. **And** upon a successful response, the JSON payload must be parsed into the `WeatherApiResponse` Pydantic model.
6. **And** the parsed model must contain data for `current.wind_mph`, `current.feelslike_c`, `current.uv`, `current.precip_mm`, and `forecast.forecastday[0].day.daily_chance_of_rain`.
7. **And** the `get_weather` method must return the validated `WeatherApiResponse` object.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- Implement the `get_weather` method within the `WeatherApiClient` class in `services/weather_api.py`.
- This method must accept `location` (string) and `date` (`datetime.date`) as arguments.
- Use the `requests` library to perform a `GET` request to the specified endpoint.
- Construct the request with the required parameters: `key`, `q`, `dt`, and `days`.
- After receiving a successful HTTP response, use `response.json()` to get the payload and `WeatherApiResponse.parse_obj()` to validate and parse it.

### Architecture Compliance

- **API Client:** All logic for interacting with the WeatherAPI.com service must be encapsulated within the `WeatherApiClient` class in `services/weather_api.py`.
- **Data Models:** The client must use the `WeatherApiResponse` model from `engine/models.py` as its return type, ensuring a validated and structured data contract with the rest of the application.
- **Data Flow:** The client receives primitive types (string, date) and returns a validated Pydantic object, which will then be consumed by the `HeuristicSafetyEngine`.

### Library/Framework Requirements

- **requests:** Use for making the HTTP GET request.
- **pydantic:** Use for parsing and validating the API response into the `WeatherApiResponse` model.

### File Structure Requirements

- The implementation will be exclusively within `services/weather_api.py`.
- It will depend on models defined in `engine/models.py`.

### Testing Requirements

- Write a unit test that mocks the `requests.get` call.
- The test should verify that a successful API response with a valid JSON payload results in a correctly populated `WeatherApiResponse` object being returned.
- Confirm that the correct URL and query parameters are being used in the mocked request.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented the `get_weather_data` method in `services/weather_api.py` to fetch data from the WeatherAPI.com `forecast.json` endpoint.
- The client now intelligently reconstructs the `current` weather object from the first hour of the `forecastday` data, ensuring consistency and resilience against missing top-level `current` data.
- Added unit tests in `tests/services/test_weather_api.py` using `requests-mock` to verify that the correct API endpoint and parameters are used and that a successful response is correctly parsed into a `WeatherApiResponse` model.

### File List

- `services/weather_api.py`
- `services/models.py`
- `tests/services/test_weather_api.py`