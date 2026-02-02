# Story 5.5: Pydantic Model Usage

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a developer, I want all data transfer objects (DTOs) to be defined using Pydantic models, so that data is validated and contracts between services are clear.

## Acceptance Criteria

1. **Given** data is passed between different services (e.g., WeatherAPI to Heuristic Engine),
2. **When** the data is received by a service,
3. **Then** it must be validated against a Pydantic model to ensure its structure and types are correct.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- **NFR1 (Data Validation):** All data structures passed between services must be validated using Pydantic models.

### Completion Notes List

- Pydantic `BaseModel` has been used consistently across the project for all data structures.
- **`services/models.py`**: Defines all models for external API interactions (`WeatherApiResponse`) and the final report structure (`AssessmentReport`, `GeminiOutput`).
- **`engine/models.py`**: Defines the data contracts for the heuristic engine's inputs and outputs (`HeuristicInput`, `HeuristicOutput`).
- **`utils/app_error.py`**: Uses a Pydantic model for the `AppErrorWrapper` to ensure standardized error structures throughout the application.
- This rigorous use of Pydantic enforces data validation at service boundaries and provides clear, self-documenting data contracts.

### File List

- `services/models.py`
- `engine/models.py`
- `utils/app_error.py`