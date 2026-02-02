# Story 5.1: Summary Report Generation

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to generate a summary report containing the raw weather metrics, the rule-based status, and the AI interpretation, so that users have a comprehensive overview.

## Acceptance Criteria

1.  **Given** a complete safety assessment has been performed (including weather data, heuristic decision, and AI explanation),
2.  **When** a report is requested,
3.  **Then** a comprehensive Pydantic model representing the full report must be generated.
4.  **And** this report model must include the following specific fields:
    *   Input `location` and `date`.
    *   Raw weather metrics: `wind_mph`, `temp_c`, `uv_index`, `pop_percent`, `precip_rate_mmhr`, `feelslike_c`.
    *   The final `HeuristicOutput.decision`.
    *   The `HeuristicOutput.weighted_score`.
    *   The `HeuristicOutput.notes`.
    *   The full AI-generated `GeminiOutput.explanation`.
    *   All individual metric categories and scores (e.g., `wind_category`, `wind_score`).
    *   A list of any `HardStopReasons`.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- **Create a `SafetyReport` Pydantic Model:** In a relevant models file (e.g., `engine/models.py`), create a new `SafetyReport` model with the following specific structure to meet the acceptance criteria:
  ```python
  # In engine/models.py
  from pydantic import BaseModel
  from typing import List, Optional, Dict
  import datetime

  # Assuming HeuristicOutput and GeminiOutput are defined elsewhere
  # and will be imported.

  class ReportInput(BaseModel):
      location: str
      date: datetime.date

  class RawWeatherMetrics(BaseModel):
      wind_mph: Optional[float]
      temp_c: Optional[float]
      uv_index: Optional[float]
      pop_percent: Optional[int]
      precip_rate_mmhr: Optional[float]
      feelslike_c: Optional[float]

  class MetricDetails(BaseModel):
      category: Optional[str]
      score: Optional[int]

  class SafetyReport(BaseModel):
      inputs: ReportInput
      raw_weather: RawWeatherMetrics
      decision: str
      weighted_score: Optional[float]
      notes: str
      explanation: str
      metric_details: Dict[str, MetricDetails]
      hard_stop_reasons: List[str]
  ```
- **Create a `ReportGenerator` Service:** Create a new file `services/report_generator.py`. This file will contain a class or function responsible for taking all the inputs (location, date, weather data, heuristic output, AI explanation) and assembling them into the final `SafetyReport` Pydantic model.
- The generator must ensure all data is correctly mapped to the fields of the `SafetyReport` model.

### Architecture Compliance

- **Service Layer:** The logic for assembling the final report should be encapsulated in a dedicated service in the `services/` layer, separating it from the UI and core engine.
- **Data Models:** The use of a comprehensive `SafetyReport` Pydantic model reinforces the project's architecture of using strictly-typed data contracts for passing information between components.

### Library/Framework Requirements

- **pydantic:** Used to define the `SafetyReport` model.

### File Structure Requirements

- The report generation logic will reside in `services/report_generator.py`.
- The new `SafetyReport` model should be defined in an appropriate models file, such as `engine/models.py`, to be co-located with other core data structures.

### Testing Requirements

- Write a unit test for the `ReportGenerator` service.
- Provide mock inputs (location, date, `WeatherApiResponse`, `HeuristicOutput`, etc.) to the generator.
- Verify that the output is a `SafetyReport` object and that all fields in the object correctly match the provided mock inputs.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Implemented the `AssessmentReport` Pydantic model in `services/models.py` to serve as the comprehensive data structure for a full safety assessment.
- Created the `ReportGenerator` service in `services/report_generator.py` to assemble data from weather, heuristic, and AI services into the `AssessmentReport` model.
- Added unit tests in `tests/services/test_report_generator.py` to verify that the report is generated correctly from mock inputs.

### File List

- `services/models.py`
- `services/report_generator.py`
- `tests/services/test_report_generator.py`