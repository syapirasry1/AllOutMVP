# Story 5.3: Persistent Local Report Logging

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As the system, I want to log every generated report to a local `data/` directory with a timestamped name, so that there is a persistent system audit trail.

## Acceptance Criteria

1.  **Given** a safety assessment has been successfully completed and a full `SafetyReport` object is available (containing inputs, raw weather, heuristic output, and AI explanation),
2.  **When** the assessment results are finalized,
3.  **Then** a copy of this full `SafetyReport` object must be serialized to JSON and saved to the `./data/` directory on the server.
4.  **And** the saved file must have a unique, timestamped name following the pattern "report_YYYYMMDD_HHMMSS.json" (e.g., "report_20260125_143000.json").
5.  **And** the file path and directory creation must use the `pathlib` module to ensure cross-platform compatibility.
6.  **And** the file format for the local log must be `.json` for structured data storage.

## Dev Notes
**DEV AGENT GUARDRAILS:**

### Technical Requirements

- Create a new file `services/file_logger.py`.
- Inside this file, create a class or function (e.g., `FileLogger`) with a method like `log_report`.
- This method should accept a `SafetyReport` Pydantic model as input.
- Use `datetime.datetime.now().strftime('%Y%m%d_%H%M%S')` to generate a unique timestamp for the filename.
- Use `pathlib.Path` to construct the full path to the log file within the `data/` directory (e.g., `Path("data") / f"report_{timestamp}.json"`).
- Ensure the `data/` directory exists using `path.parent.mkdir(parents=True, exist_ok=True)`.
- Serialize the `SafetyReport` object to a JSON string using its `.json(indent=4)` method for readability.
- Write the JSON string to the specified file.

### Architecture Compliance

- **Service Layer:** This functionality must be encapsulated in a dedicated service within the `services/` directory, separating file I/O from the main application logic.
- **Persistent Log:** This story directly implements the "Persistent Log" half of the dual-output system defined in the architecture.
- **Cross-Platform Compatibility:** The mandatory use of `pathlib` fulfills the architectural requirement for a cross-platform solution (Windows/macOS).

### Library/Framework Requirements

- **pathlib:** For constructing file system paths.
- **datetime:** For generating timestamps.
- **pydantic:** For serializing the report model to JSON.

### File Structure Requirements

- The implementation logic will reside in `services/file_logger.py`.
- The service will write files to the `data/` directory in the project root.

### Testing Requirements

- Write a unit test for the `FileLogger` service.
- The test should call the `log_report` method with a mock `SafetyReport` object.
- Use mocking (`unittest.mock.patch`) to intercept the file-writing operation (`Path.write_text`).
- Verify that the mocked `write_text` function is called with the correctly formatted JSON string.
- Verify that the path passed to the mocked file operation is correctly constructed with the `data/` directory and a timestamped filename.

### Project Context Reference

For broader project context, refer to:
[Project Context Document](../../_bmad-output/planning-artifacts/project-context.md)

## Dev Agent Record

### Agent Model Used

sm-1.0

### Completion Notes List

- Created the `log_report_to_file` function in `services/file_logger.py` to handle the serialization and saving of assessment reports.
- The implementation uses `pathlib` for cross-platform path construction and ensures the `data/` directory is created if it doesn't exist.
- The service now saves the `AssessmentReport` as a JSON file with a timestamped name (e.g., `report_YYYYMMDD_HHMMSS.json`).
- Added unit tests in `tests/services/test_file_logger.py` using `tmp_path` to validate file creation and content without writing to the actual file system.

### File List

- `services/file_logger.py`
- `tests/services/test_file_logger.py`