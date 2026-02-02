# Project Backlog: AllOut MVP

This document outlines the complete, finalized project backlog for the AllOut Minimum Viable Product (MVP), including all Epics, User Stories, and their detailed Acceptance Criteria, incorporating all discussions and refinements.

---

## Epic 1: User Interface & Core Interaction
**Goal:** Provide an intuitive web interface for users to get safety assessments.

*   ### User Story 1.1: Anonymous Access
    *   **Story:** As an outdoor enthusiast, I want to access AllOut without logging in, so that I can quickly check conditions.
    *   **Acceptance Criteria:**
        *   **Given** any user navigates to the application URL,
        *   **When** AllOut loads,
        *   **Then** the user must be able to see and interact with the core features (location input, date selection, and assessment button) without any login or authentication prompt.

*   ### User Story 1.2: Location Input
    *   **Story:** As an outdoor enthusiast, I want to input a specific geographical location, so that I can get relevant safety information for my activity.
    *   **Acceptance Criteria:**
        *   **Given** the main application interface is displayed,
        *   **When** the user looks at the screen,
        *   **Then** a text input field for "Location" must be clearly visible.
        *   **And** the input field must default to "Coventry".
        *   **And** the user must be able to type a location (e.g., city, zip/postcode, or lat/lon coordinates) into this field.
        *   **And** all user-provided location strings must be validated and sanitized to prevent security vulnerabilities (e.g., injection attacks).
        *   **And** if the input is deemed invalid or unsafe, an appropriate user-facing error message should be displayed.

*   ### User Story 1.3: Date Selection
    *   **Story:** As an outdoor enthusiast, I want to select a date for my planned activity, so that the assessment reflects conditions at that specific time.
    *   **Acceptance Criteria:**
        *   **Given** the main application interface is displayed,
        *   **When** the user looks at the screen,
        *   **Then** a date selection widget must be clearly visible, defaulting to today's date.
        *   **And** the user must be able to select today's date or a future date from this widget.

*   ### User Story 1.4: Visual Safety Indicator
    *   **Story:** As an outdoor enthusiast, I want to see a clear visual indicator of the safety status (Green/Amber/Red), so that I can quickly understand the overall risk.
    *   **Acceptance Criteria:**
        *   **Given** a safety assessment has been successfully completed,
        *   **When** the `HeuristicOutput.decision` is "GO",
        *   **Then** a prominent visual indicator for "GO" (e.g., a green-colored container with an icon like a checkmark and the text "GO") must be displayed.
        *   **When** the `HeuristicOutput.decision` is "MAYBE",
        *   **Then** a prominent visual indicator for "MAYBE" (e.g., an amber/orange-colored container with an icon like a warning sign and the text "MAYBE") must be displayed.
        *   **When** the `HeuristicOutput.decision` is "NO-GO",
        *   **Then** a prominent visual indicator for "NO-GO" (e.g., a red-colored container with an icon like an X or a stop sign and the text "NO-GO") must be displayed.
        *   **When** the `HeuristicOutput.decision` is "INSUFFICIENT DATA" or "NO DATA",
        *   **Then** a neutral-colored indicator (e.g., grey) must be displayed with the corresponding status text.

*   ### User Story 1.5: Fast Initial Load Time
    *   **Story:** As an outdoor enthusiast, I want a responsive application that loads quickly, so that I don't waste time waiting for the page to appear.
    *   **Acceptance Criteria:**
        *   **Given** a user with a standard broadband connection navigates to the application URL,
        *   **When** the application is loading for the first time,
        *   **Then** the core UI structure (input fields, buttons) must be rendered in **under 2 seconds** (NFR2).

*   ### User Story 1.6: Loading Feedback
    *   **Story:** As an outdoor enthusiast, I want to see a loading indicator when the system is processing my request, so that I know the application is working.
    *   **Acceptance Criteria:**
        *   **Given** a user has entered a location and date,
        *   **When** they click the "Assess" button and the system is fetching data and generating an explanation,
        *   **Then** a spinner or similar loading indicator must be displayed to show the application is working.
        *   **And** this loading indicator must disappear once the final assessment results are displayed.

---

## Epic 2: Weather Data Integration & Management
**Goal:** Reliably fetch and process external weather data for accurate assessments.

*   ### User Story 2.1: Fetch Weather Data (WeatherAPI.com)
    *   **Story:** As the system, I want to fetch required weather data from WeatherAPI.com, so that the safety assessment can be performed.
    *   **Acceptance Criteria:**
        *   **Given** a valid location (e.g., "London") and an API key,
            *   **When** a request is made for the current weather,
            *   **Then** the system must make a `GET` request to the `api.weatherapi.com` forecast endpoint.
            *   **And** the response must be successfully parsed into the `WeatherApiResponse` Pydantic model.
            *   **And** the parsed model must contain data for `current.wind_mph`, `current.feelslike_c`, `current.uv`, `current.precip_mm`, and `forecast.forecastday[0].day.daily_chance_of_rain`.
        *   **Given** a valid location and a specific date (either today or a future date),
            *   **When** a request is made for weather data for that date,
            *   **Then** the system must make a `GET` request to the `api.weatherapi.com` forecast endpoint, including the `q` (location) and `dt` (date) parameters.
            *   **And** the `days` parameter must be set to `1` to retrieve data for the specific day.
            *   **And** the response must be successfully parsed into the `WeatherApiResponse` Pydantic model.
            *   **And** the parsed model must contain data for `current.wind_mph`, `current.feelslike_c`, `current.uv`, `current.precip_mm`, and `forecast.forecastday[0].day.daily_chance_of_rain` relevant to the requested date.
        *   **Given** the Weather API returns a response that is syntactically valid against the `WeatherApiResponse` Pydantic model,
            *   **When** the `WeatherApiClient` processes this response,
            *   **Then** the `WeatherApiClient` must successfully return the `WeatherApiResponse` object, regardless of whether the *number* of available metrics is sufficient for the heuristic engine.
            *   **And** the determination of "INSUFFICIENT DATA" must be left to the Heuristic Safety Engine.

*   ### User Story 2.2: API Timeout Handling
    *   **Story:** As the system, I want to handle complete weather API timeouts or unavailability, so that the user receives an informative error message.
    *   **Acceptance Criteria:**
        *   **Given** the Weather API service does not respond within the defined timeout (e.g., 5 seconds),
            *   **When** a weather data request is made,
            *   **Then** an `AppErrorWrapper` exception must be raised with the `error_code` "WEATHERAPI_TIMEOUT".
            *   **And** the `user_message` must be "Weather service request timed out. Please try again later."
        *   **Given** the system cannot establish a network connection to the Weather API service,
            *   **When** a weather data request is made,
            *   **Then** an `AppErrorWrapper` exception must be raised with the `error_code` "WEATHERAPI_CONNECTION_ERROR".
            *   **And** the `user_message` must be "Could not connect to the weather service. Please check your internet connection."

*   ### User Story 2.3: Partial Data Handling
    *   **Story:** As the system, I want to handle situations where specific, **critical** data fields are unexpectedly missing from the API response, leading to a parsing error.
    *   **Acceptance Criteria:**
        *   **Given** the Weather API returns a syntactically valid response, but a field defined as **non-optional and critical** in the `WeatherApiResponse` Pydantic model (e.g., `current` block itself, or `wind_mph` if we were to make it non-optional) is missing from the payload,
            *   **When** the response is parsed,
            *   **Then** a Pydantic `ValidationError` must be caught during parsing.
            *   **And** an `AppErrorWrapper` exception must be raised with the `error_code` "WEATHERAPI_SCHEMA_CHANGE_MISSING_FIELDS".
            *   **And** the `user_message` must contain the text "Missing or invalid fields:" followed by the name of the missing field (e.g., "current.uv" if it were required).

*   ### User Story 2.4: API Schema Change Detection
    *   **Story:** As the system, I want to detect fundamental structural changes in the API response that prevent successful parsing, so that the assessment halts and an appropriate message is displayed.
    *   **Acceptance Criteria:**
        *   **Given** the Weather API returns a response with a structure that **fundamentally does not match** the `WeatherApiResponse` Pydantic model (e.g., top-level keys are renamed, or critical blocks are entirely absent),
            *   **When** the response is parsed,
            *   **Then** a Pydantic `ValidationError` must be caught.
            *   **And** an `AppErrorWrapper` exception must be raised with an `error_code` like "WEATHERAPI_SCHEMA_CHANGE".
            *   **And** the `user_message` must be "Weather service returned data in an unexpected format."

*   ### User Story 2.5: Secure API Key Storage
    *   **Story:** As the system, I want to store API keys securely, so that sensitive credentials are not exposed.
    *   **Acceptance Criteria:**
        *   **Given** the application is running,
            *   **When** the `WeatherApiClient` is initialized,
            *   **Then** it must load the API key from an environment variable named `WEATHERAPI_KEY` (or a `.env` file).
        *   **Given** the `WEATHERAPI_KEY` is not found in the environment,
            *   **When** the `WeatherApiClient` is initialized,
            *   **Then** an `AppErrorWrapper` with error code `WEATHERAPI_KEY_MISSING` must be raised.
        *   **Given** any source code file in the project,
            *   **Then** no file shall contain a hard-coded API key.

---

## Epic 3: Heuristic Safety Engine
**Goal:** Accurately and deterministically assess outdoor safety based on weather conditions.

*   ### User Story 3.1: Rule-Based Safety Assessment
    *   **Story:** As the system, I want to evaluate fetched weather data against pre-defined safety thresholds, so that I can determine a Green, Amber, or Red safety status.
    *   **Acceptance Criteria (Consolidated):**

        **Scenario: Metric Availability and Initial Checks**
        *   **Given** an input with `wind_mph`, `heat_index_c`, `wind_chill_c`, `uv_index`, `pop_percent`, and `precip_rate_mmhr`,
            *   **When** the engine runs,
            *   **Then** `wind_available` is true if `wind_mph` is not missing.
            *   **And** `thermal_available` is true if `heat_index_c` OR `wind_chill_c` is not missing.
            *   **And** `uv_available` is true if `uv_index` is not missing.
            *   **And** `precip_available` is true if `pop_percent` is not missing.
            *   **And** `available_metric_count` is the count of true availability flags for the 4 combined metrics (Wind, Thermal, UV, Precip).
            *   **And** `missing_metrics` lists the metric names where availability is false.

        *   **Given** `available_metric_count = 0`,
            *   **When** the engine runs,
            *   **Then** the final `Decision` must be "NO DATA".
            *   **And** `notes` must be "No weather metrics available. Cannot assess conditions."
            *   **And** `weighted_score` must be null.
        *   **Given** `available_metric_count = 1`,
            *   **When** the engine runs,
            *   **Then** the final `Decision` must be "INSUFFICIENT DATA".
            *   **And** `notes` must be "Only 1 metric available. Cannot compute GO/MAYBE/NO-GO reliably. At least 2 metrics needed."
            *   **And** the output should transparently include the 1 available metric.

        **Scenario: Metric Categorization (Applied if metric is available and `available_metric_count >= 2`)**

        *   **Wind Category (`wind_mph`):**
            *   **Given** `wind_mph < 20`, **Then** `wind_category` is Green.
            *   **Given** `20 <= wind_mph < 32`, **Then** `wind_category` is Amber.
            *   **Given** `wind_mph >= 32`, **Then** `wind_category` is Red.

        *   **Thermal Stress Category (`heat_index_c`, `wind_chill_c`):**
            *   **Given** `heat_index_c` is not missing and `>= 27`:
                *   **When** `heat_index_c < 27`, **Then** `thermal_stress_category` is Green.
                *   **When** `27 <= heat_index_c < 41`, **Then** `thermal_stress_category` is Amber.
                *   **When** `heat_index_c >= 41`, **Then** `thermal_stress_category` is Red.
            *   **Else if** `wind_chill_c` is not missing and `<= -10`:
                *   **When** `wind_chill_c > -10`, **Then** `thermal_stress_category` is Green.
                *   **When** `-28 < wind_chill_c <= -10`, **Then** `thermal_stress_category` is Amber.
                *   **When** `wind_chill_c <= -28`, **Then** `thermal_stress_category` is Red.
            *   **Else** (mild temperatures), **Then** `thermal_stress_category` is Green.

        *   **UV Category (`uv_index`):**
            *   **Given** `uv_index <= 2`, **Then** `uv_category` is Green.
            *   **Given** `3 <= uv_index <= 7`, **Then** `uv_category` is Amber.
            *   **Given** `uv_index >= 8`, **Then** `uv_category` is Red.

        *   **Precipitation Category (`pop_percent`, `precip_rate_mmhr`) (Rate Dominates):**
            *   **Step D1 (PoP Category):**
                *   **Given** `pop_percent <= 20`, **Then** `pop_category` is Green.
                *   **Given** `21 <= pop_percent <= 50`, **Then** `pop_category` is Amber.
                *   **Given** `pop_percent > 50`, **Then** `pop_category` is Red.
            *   **Step D2 (Precipitation Rate Category):**
                *   **Given** `pop_percent <= 20`, **Then** `precip_rate_category` is Green.
                *   **Else if** `pop_percent > 20` AND `precip_rate_mmhr` is missing, **Then** `precip_rate_category` is Amber.
                *   **Else if** `pop_percent > 20` AND `precip_rate_mmhr` is available:
                    *   **When** `precip_rate_mmhr < 0.5`, **Then** `precip_rate_category` is Green.
                    *   **When** `0.5 <= precip_rate_mmhr <= 4.0`, **Then** `precip_rate_category` is Amber.
                    *   **When** `precip_rate_mmhr > 4.0`, **Then** `precip_rate_category` is Red.
            *   **Step D3 (Combined Precipitation Score):**
                *   **Given** `pop_percent <= 20`, **Then** the final `precip_score` is 100 (Green).
                *   **Else if** `pop_percent > 20`, **Then** the final `precip_score` is determined solely by the score of the `precip_rate_category`.

        **Scenario: Score Mapping and Weighting (No Renormalization, Rounded Precision)**
        *   **Given** a `wind_category`, `thermal_stress_category`, `uv_category`, `precip_category` (for available metrics),
            *   **When** mapping categories to scores,
            *   **Then** Green maps to 100, Amber to 50, and Red to 0 for `wind_score`, `thermal_stress_score`, `uv_score`, and `precip_score`.
        *   **Given** `wind_weight=0.20`, `thermal_weight=0.35`, `precip_weight=0.40`, `uv_weight=0.05`,
            *   **When** `available_metric_count >= 2`,
            *   **Then** `WeightedScore_calculated` is computed as the direct sum of `(metric_score * metric_weight)` for ONLY the available metrics.
            *   **And** `WeightedScore_0_100` is computed as `ROUND(WeightedScore_calculated, 2)`.

        **Scenario: Hard-Stop Rules (Applied if `available_metric_count >= 2`)**
        *   **Given** any of the following conditions are met:
            *   `wind_available` AND `wind_mph >= 32`
            *   `heat_index_c` NOT missing AND `heat_index_c >= 41`
            *   `wind_chill_c` NOT missing AND `wind_chill_c <= -28`
            *   `pop_percent` NOT missing AND `pop_percent > 20` AND `precip_rate_mmhr` NOT missing AND `precip_rate_mmhr > 4.0`
        *   **When** the engine runs,
        *   **Then** `HardStop` must be TRUE.
        *   **And** `HardStopReasons` must list all triggered conditions.
        *   **Note:** UV Index DOES NOT trigger a hard-stop rule, even at extreme levels.

        **Scenario: Final Decision Logic (Applied if `available_metric_count >= 2`)**
        *   **Given** `HardStop == TRUE`, **Then** `Decision` is "NO-GO".
        *   **Else if** `WeightedScore_0_100` (rounded to 2 decimal places) `>= 75`, **Then** `Decision` is "GO".
        *   **Else if** `50 <= WeightedScore_0_100` (rounded to 2 decimal places) `< 75`, **Then** `Decision` is "MAYBE".
        *   **Else** (`WeightedScore_0_100` (rounded to 2 decimal places) `< 50`), **Then** `Decision` is "NO-GO".

        **Scenario: Output Notes**
        *   **Given** `available_metric_count >= 2` AND `available_metric_count < 4`,
            *   **Then** the `notes` must start with "PROVISIONAL RESULT: only [X]/4 metrics available ([list of missing metrics] missing). Proceed with general caution."
        *   **Given** `available_metric_count == 4`,
            *   **Then** the `notes` must start with "Full-data result."
        *   **And** if `uv_category` is Red, the `notes` should also include the warning: "High UV index detected. Use SPF 30+ sunscreen and protective eyewear."
        *   **And** if `uv_category` is Amber, the `notes` should also include the warning: "Moderate UV index detected. Consider using sunscreen and protective eyewear."

        **Scenario: Comprehensive Output**
        *   **When** the engine completes,
        *   **Then** the output must include: `Decision`, `WeightedScore_0_100` (if applicable), `Notes`, `available_metric_count`, `missing_metrics` (list), `MetricCategories` (only for available metrics), `MetricScores` (only for available metrics), `HardStop` (true/false), and `HardStopReasons` (list).

### Epic 4: AI Decision Support & Interpretation
**Goal:** Provide clear, conversational explanations that align with heuristic safety assessments.

*   ### User Story 4.1: LLM-Powered Conversational Explanation
    *   **Story:** As the system, I want to generate a conversational explanation of the safety status using an LLM, so that users understand the "so what" of the weather data.
    *   **Acceptance Criteria:**
        *   **Given** a `GeminiInput` object containing `HeuristicOutput` and relevant weather data (`CurrentWeather`, `DayForecast`),
            *   **When** the `GeminiLLMClient`'s `get_explanation` method is called,
            *   **Then** a prompt must be constructed using the provided `location_name`, current weather details (`temp_c`, `feelslike_c`, `wind_mph`, `precip_mm`, `uv`), forecast details (`daily_chance_of_rain`, if available), and the full `HeuristicOutput` (Decision, Weighted Score, Notes, Metric Categories, Hard Stop Reasons).
            *   **And** the prompt must clearly instruct the LLM to provide a **concise, conversational explanation** that **strictly aligns with the `HeuristicOutput.decision`** and **NEVER contradicts it**.
            *   **And** the explanation should be under 150 words.
            *   **And** the system must make a call to the configured Gemini model (`gemini-2.5-flash`).
            *   **And** the LLM's response must be successfully parsed into a `GeminiOutput` Pydantic model containing the explanation text.
        *   **Given** the LLM returns an explanation,
            *   **When** `HeuristicOutput.decision` is "GO",
            *   **Then** the explanation should justify the "GO" decision and may include general safety reminders.
        *   **Given** the LLM returns an explanation,
            *   **When** `HeuristicOutput.decision` is "MAYBE" or "NO-GO",
            *   **Then** the explanation should clearly highlight the key risks and reasons for the caution/no-go decision.
        *   **Given** the `GEMINI_API_KEY` is not found in the environment,
            *   **When** the `GeminiLLMClient` is initialized,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_API_KEY_MISSING" must be raised.
        *   **Given** the Gemini API returns an error during content generation,
            *   **When** `get_explanation` is called,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_API_ERROR" must be raised.
        *   **Given** the prompt to the LLM is blocked by Gemini's safety settings,
            *   **When** `get_explanation` is called,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_PROMPT_BLOCKED" must be raised.
        *   **Given** the LLM's generated response is blocked by Gemini's safety settings,
            *   **When** `get_explanation` is called,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_RESPONSE_BLOCKED" must be raised.
        *   **Given** the Gemini API returns an empty explanation (no text),
            *   **When** `get_explanation` is called,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_EMPTY_RESPONSE" must be raised.
        *   **Given** any other unexpected error occurs during Gemini interaction,
            *   **When** `get_explanation` is called,
            *   **Then** an `AppErrorWrapper` with `error_code` "GEMINI_UNEXPECTED_ERROR" must be raised.

*   ### User Story 4.2: Low AI Response Latency
    *   **Story:** As an outdoor enthusiast, I want to receive the AI-powered safety explanation quickly, so that I can make timely decisions.
    *   **Acceptance Criteria:**
        *   **Given** a valid request is sent to the Gemini LLM for an explanation,
            *   **When** the LLM client receives the response,
            *   **Then** the time taken from sending the request to receiving the full explanation must be **under 6.5 seconds** (NFR1).

### Epic 5: Report Generation & Persistence
**Goal:** Allow users to save and review safety reports, and maintain an internal audit trail.

*   ### User Story 5.1: Summary Report Generation
    *   **Story:** As the system, I want to generate a summary report containing the raw weather metrics, the rule-based status, and the AI interpretation, so that users have a comprehensive overview.
    *   **Acceptance Criteria:**
        *   **Given** a complete safety assessment has been performed (including weather data, heuristic decision, and AI explanation),
            *   **When** a report is requested,
            *   **Then** the generated report must include:
                *   The input location and date.
                *   Raw weather metrics (e.g., `wind_mph`, `temp_c`, `uv_index`, `pop_percent`, `precip_rate_mmhr`, `feelslike_c`).
                *   The final `HeuristicOutput.decision` (GO/MAYBE/NO-GO/INSUFFICIENT DATA/NO DATA).
                *   The `HeuristicOutput.weighted_score` (rounded to 2 decimal places, if applicable).
                *   The `HeuristicOutput.notes` (including provisional status and UV warnings).
                *   The full AI-generated `GeminiOutput.explanation`.
                *   All individual metric categories (Wind, Thermal, UV, Precip) and their scores.
                *   Any `HardStopReasons`.

*   ### User Story 5.2: User Report Export
    *   **Story:** As an outdoor enthusiast, I want to save/export the generated safety report as a local `.txt` or `.json` file, so that I can keep a record for future reference.
    *   **Acceptance Criteria:**
        *   **Given** a summary report has been generated and is displayed,
            *   **When** the user clicks an "Export" or "Download" button,
            *   **Then** the report content must be provided to the user as a downloadable file.
            *   **And** the user must have the option to save the file in `.txt` format.
            *   **And** the user must have the option to save the file in `.json` format.
            *   **And** the filename should be unique and reflect the assessment (e.g., "AllOut_London_2026-01-25.json").

*   ### User Story 5.3: Persistent Local Report Logging
    *   **Story:** As the system, I want to log every generated report to a local `data/` directory with a timestamped name, so that there is a persistent system audit trail.
    *   **Acceptance Criteria:**
        *   **Given** a safety assessment has been successfully completed,
            *   **When** the assessment results are finalized,
            *   **Then** a copy of the full report (including inputs, raw weather, heuristic output, and AI explanation) must be saved to the `./data/` directory on the server.
            *   **And** the saved file must have a unique, timestamped name (e.g., "report_YYYYMMDD_HHMMSS.json" or "report_YYYYMMDD_HHMMSS.txt").
            *   **And** the saving mechanism must use `pathlib` to ensure cross-platform compatibility.
            *   **And** the file format for local logging should be `.json` for structured data storage.

*   ### User Story 5.4: ISO 8601 UTC Date/Time Format
    *   **Story:** As the system, I want to ensure all internal processing and logging uses ISO 8601 UTC format for dates and times, so that there are no ambiguity issues.
    *   **Acceptance Criteria:**
        *   **Given** any date or time information is used internally (e.g., for logging timestamps, internal report fields),
            *   **When** this information is generated or stored,
            *   **Then** it must strictly adhere to the ISO 8601 format in UTC (e.g., `YYYY-MM-DDTHH:MM:SSZ`).
        *   **Given** any date or time information is displayed to the user,
            *   **When** it is converted from internal UTC format,
            *   **Then** it must be converted to the user's local time format for convenience.

*   ### User Story 5.5: Pydantic Model Usage
    *   **Story:** As the system, I want to use Pydantic models for all internal data structures and API responses, so that data integrity is maintained and validation is strict.
    *   **Acceptance Criteria:**
        *   **Given** data is passed between system components (e.g., from Weather API Client to Heuristic Engine, Heuristic Engine to Gemini LLM, or to Report Generator),
            *   **When** the data represents structured information,
            *   **Then** it must be encapsulated and validated by appropriate Pydantic models.
        *   **Given** an external API response is received (e.g., from WeatherAPI.com),
            *   **When** this response is processed,
            *   **Then** it must be parsed and validated using a Pydantic model (`WeatherApiResponse`).
        *   **Given** an internal application error occurs,
            *   **When** it is represented for logging or display,
            *   **Then** it must use the `AppError` Pydantic model for consistency.