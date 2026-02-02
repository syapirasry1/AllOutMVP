# Story 3.1: Rule-Based Safety Assessment

Status:  **DONE** (v3.0.0)

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to evaluate fetched weather data against pre-defined safety thresholds, so that I can determine a Green, Amber, or Red safety status.

## Acceptance Criteria (Consolidated)

1.  **Given** a `WeatherApiResponse` object, the `HeuristicSafetyEngine` must evaluate it. ✅
2.  **Metric Categorization:** Each available metric must be categorized as Green, Amber, or Red based on the following thresholds: ✅
    *   **Wind (`wind_mph`):** Green `< 20`, Amber `< 32`, Red `>= 32`. ✅
    *   **Thermal Stress (`feelslike_c`):** ✅
        *   Heat (`>= 27°C`): Green `< 27`, Amber `< 41`, Red `>= 41`. ✅
        *   Cold (`<= -10°C`): Green `> -10`, Amber `> -28`, Red `<= -28`. ✅
        *   Mild: Green. ✅
    *   **UV (`uv_index`):** Green `< 3`, Amber `< 8`, Red `>= 8`. ✅
    *   **Precipitation (`pop_percent`, `precip_rate_mmhr`):** ✅
        *   If PoP `<= 20%`, then Green. ✅
        *   If PoP `> 20%`, then rate dominates: Green `< 0.5`, Amber `<= 4.0`, Red `> 4.0`. If rate is unavailable, defaults to Amber. ✅
3.  **Metric Scoring:** Categories must be mapped to scores: Green = 100, Amber = 50, Red = 0. ✅
4.  **Weighted Score Calculation (No Renormalization Rule):** ✅
    *   **Given** weights: Wind (0.20), Thermal (0.35), Precip (0.40), UV (0.05). ✅
    *   **When** calculating the final score, the calculation must be a direct sum of `(metric_score * metric_weight)` for **only the available metrics**. The weights of missing metrics are ignored and the total weight is not renormalized. ✅
5.  **Hard-Stop Rules:** The assessment must immediately result in a "NO-GO" if any of these are true: ✅
    *   `wind_mph >= 32`. ✅
    *   `feelslike_c >= 41` (Extreme Heat). ✅
    *   `feelslike_c <= -28` (Extreme Cold). ✅
    *   `precip_rate_mmhr > 4.0` (when PoP > 20%). ✅
6.  **Final Decision Logic:** ✅
    *   If a Hard-Stop is triggered, the decision is "NO-GO". ✅
    *   Else if weighted score `>= 75`, the decision is "GO". ✅
    *   Else if `50 <=` weighted score `< 75`, the decision is "MAYBE". ✅
    *   Else, the decision is "NO-GO". ✅
7.  **Output:** The engine must return a populated `HeuristicOutput` model containing the final decision, weighted score, notes, and a list of any hard-stop reasons. ✅

## Implementation Summary (v3.0.0)

### Files Modified
- `engine/heuristic_engine.py` - Core safety assessment logic
- `engine/models.py` - HeuristicInput and HeuristicOutput models
- `tests/engine/test_heuristic_engine.py` - Comprehensive test coverage

### Key Features Implemented
- Metric categorization (Wind, Thermal, UV, Precipitation)
- Hard-stop safety rules (immediate NO-GO conditions)
- Weighted score calculation without renormalization
- Decision logic (GO/MAYBE/NO-GO)
- Edge case handling (NO DATA, INSUFFICIENT DATA)

### Test Coverage
All test scenarios passing:
- ✅ Perfect conditions → GO
- ✅ Marginal conditions → MAYBE
- ✅ Poor conditions → NO-GO
- ✅ Wind hard-stop (≥32 mph)
- ✅ Thermal hard-stops (≥41°C, ≤-28°C)
- ✅ Precipitation hard-stop (>4.0 mm/hr)
- ✅ Multiple hard-stops
- ✅ No data scenario
- ✅ Insufficient data scenario
- ✅ Partial data score calculation

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- Implement the `run` method within the `HeuristicSafetyEngine` class in `engine/heuristic_engine.py`. ✅
- The method must accept a `WeatherApiResponse` object. ✅
- Implement private helper methods for categorizing each metric (`_categorize_wind`, `_categorize_thermal_stress`, etc.) according to the specific thresholds in the Acceptance Criteria. ✅
- The `run` method must orchestrate the calls to categorization, scoring, weighting, hard-stop checks, and final decision logic. ✅
- Ensure the final weighted score is calculated without renormalization, as per the explicit rule. ✅

### Architecture Compliance

- **Business Logic:** This story represents the core business logic of the application. All of this logic must be encapsulated within the `HeuristicSafetyEngine` in the `engine/` layer, completely separate from the UI (`app.py`) and external services (`services/`). ✅
- **Data Models:** The engine must accept `WeatherApiResponse` and return `HeuristicOutput` as defined in `engine/models.py`, respecting the data contracts between components. ✅

### Library/Framework Requirements

- No external libraries are required; this implementation relies on standard Python and the project's Pydantic models. ✅

### File Structure Requirements

- The implementation will be exclusively within `engine/heuristic_engine.py`. ✅
- It will depend on models defined in `engine/models.py`. ✅

### Testing Requirements

- Write unit tests for each private categorization method to ensure thresholds are applied correctly. ✅
- Write a comprehensive test for the `run` method for each decision scenario (GO, MAYBE, NO-GO). ✅
- Write a specific test to verify that the "No Renormalization" rule is correctly applied when a metric is missing. ✅
- Write a test for each Hard-Stop condition to ensure it correctly overrides the weighted score and results in a "NO-GO" decision. ✅
- Write tests for the "NO DATA" (0 metrics) and "INSUFFICIENT DATA" (1 metric) edge cases. ✅

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0 (Planning)
Claude Sonnet 4.5 (Implementation)

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created
- Story 3.1 fully implemented in v3.0.0
- All metric categorization logic implemented
- Hard-stop rules working correctly
- Weighted scoring without renormalization verified
- Comprehensive test suite passing (13 heuristic engine tests)
- Edge cases handled (NO DATA, INSUFFICIENT DATA)

### File List

**Implemented:**
- `engine/heuristic_engine.py` - Main heuristic safety engine
- `engine/models.py` - Input/output data models
- `tests/engine/test_heuristic_engine.py` - Complete test suite

**Git Tag:** v3.0.0

**Release Date:** 2026-01-27 (estimated based on development timeline)