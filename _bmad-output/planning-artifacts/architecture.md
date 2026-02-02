---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-01-24'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._
## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
The core functional requirements revolve around a decision-support tool that takes user-provided location and date, fetches external weather data, and processes it through a two-tiered assessment. The first tier is a deterministic, rule-based heuristic engine determining a Green/Amber/Red safety status. The second tier involves an LLM (Gemini) generating a conversational explanation of this status, ensuring the LLM never overrides the heuristic decision. Key functions include anonymous access, input validation, comprehensive API error handling (timeout, partial data, schema changes), and the ability to generate and export a summary report.

**Non-Functional Requirements:**
Key non-functional requirements emphasize performance with strict latency targets for AI response (<6.5s), initial SPA load (<2s), and API data retrieval (<1.5s). Security is paramount, mandating secure API key storage via `.env` files and robust input sanitization. Maintainability is addressed through adherence to PEP 8, meaningful variable names, and inline comments for logic explanation. Accessibility requires color-blind friendly visual indicators. Compatibility spans modern OS (Windows 10+, macOS latest two) and major browsers (Chrome, Firefox, Safari).

**Scale & Complexity:**
The project is categorized as having **low complexity**, focusing on a problem-solving MVP with a strong experience focus. The primary goal is to bridge the "interpretation gap" in outdoor environmental data.

- Primary domain: Web Application (Full-stack, with the entire application including the UI implemented in Python using a suitable web framework like Streamlit, Dash, or FastAPI with server-side templating).
- Complexity level: Low
- Estimated architectural components: The system will likely involve distinct components for the UI rendering, a backend for handling requests, weather data fetching and parsing, the heuristic safety engine, and the LLM integration layer, all within a single Python application.

### Technical Constraints & Dependencies

The system is constrained by its reliance on an external weather data provider API and the Gemini 2.5 Flash Layer for AI interpretation. The entire application stack, including the user interface, is mandated to be implemented in Python. API keys must be managed through `.env` files to ensure security and ease of testing, **utilizing standard Python libraries for API calls and secure configuration management.**

### Cross-Cutting Concerns Identified

*   **Error Handling:** Critical for robust operation, particularly concerning external weather API calls (timeout, partial data, schema changes). The system needs defined responses for each scenario.
*   **Security:** Encompasses secure API key management and stringent input sanitization to prevent common vulnerabilities.
*   **Performance:** Crucial for user experience, with explicit latency targets for AI, UI, and data fetching operations that will influence technology and design choices.
*   **Accessibility:** The design of visual indicators must accommodate color-blind users, ensuring critical safety information is conveyed effectively to all.
*   **Consistency between Heuristic and LLM:** A fundamental architectural challenge is ensuring the AI explanation always aligns with and never contradicts the deterministic safety assessment.

## Starter Template Evaluation

### Primary Technology Domain

Based on the project requirements analysis and our discussion, the primary technology domain is a **Full-stack Web Application implemented entirely in Python**.

### Starter Options Considered

Several Python web frameworks were evaluated, including Streamlit, Dash, FastAPI with Jinja2, and Flask with Jinja2.

### Selected Starter: Streamlit

**Rationale for Selection:**
Streamlit was chosen for its exceptional development speed and its focus on data-centric applications. This aligns perfectly with the goal of creating a "Problem-Solving MVP" for "AllOut" efficiently. Its simple, script-like nature and built-in components allow us to focus on the core heuristic engine and LLM integration, rather than on complex UI setup. The framework's architecture is well-suited to the project's low complexity and decision-support function.

**Initialization Command:**
Streamlit does not use a boilerplate generator command. Instead, a project is initialized by installing the library and creating a structured application. The following commands represent the project setup:

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# 2. Install necessary libraries
pip install streamlit

# 3. Create the main application file
touch app.py

# 4. Run the application
streamlit run app.py
```

### Architectural Decisions Provided by Starter

**Language & Runtime:**
- **Python 3.x**: The application will be built using a modern version of Python.
- **`requirements.txt`**: A `requirements.txt` file will be used to manage all project dependencies, ensuring reproducible environments.

**Styling Solution:**
- **Default Components**: The UI will primarily be built using Streamlit's standard, pre-built components.
- **Custom CSS**: An `assets/` directory can be used to include custom CSS for minor styling adjustments if necessary.

**Build Tooling:**
- **Streamlit CLI**: The `streamlit` command-line interface serves as the primary tool for running, debugging, and managing the application. No separate build or compilation step is required.

**Testing Framework:**
- **Pytest**: While Streamlit doesn't have an integrated testing solution for the UI itself, all business logic, helper functions, and the heuristic engine will be tested using `pytest` to ensure correctness.

**Code Organization:**
The project will follow a modular structure to ensure maintainability:
- `app.py`: The main entry point of the application.
- `pages/`: For creating a multi-page experience if needed in the future.
- `utils/` or `services/`: For reusable utility functions, such as API clients for the weather service and the Gemini LLM.
- `engine/`: A dedicated module for the core heuristic safety engine logic.
- `data/`: A directory for runtime-generated report logs.

**File Output and Logging:**
- **Dual-Output System**: The application will generate reports in two ways simultaneously.
- **1. User Download**: A `st.download_button` in the UI will provide the user with a convenient browser-side download of the report (`.txt` or `.json`).
- **2. Persistent Log**: Every report generated will also be written to the server's local `./data/` directory. This will serve as a persistent system log of all assessments, with each file having a unique, timestamped name to prevent overwrites. This explicitly satisfies the project's file operation requirement.

**Development Experience:**
- **Hot Reloading**: The `streamlit run` command provides built-in hot reloading, automatically updating the application in the browser when code is saved.

**Note:** Project initialization using this structure should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
These decisions are fundamental and must be made before implementation can begin.

*   **External Weather API Provider:** WeatherAPI.com
*   **Hosting Strategy:** Local Deployment via `venv` and `requirements.txt` with cross-OS file handling.

**Important Decisions (Shape Architecture):**
These decisions significantly influence the system's design but may evolve.

*   (No additional important decisions beyond those established by the Streamlit starter template and Python-only constraint for the MVP.)

**Deferred Decisions (Post-MVP):**
These decisions are not critical for the MVP and can be addressed in future phases.

*   **CI/CD Pipeline Approach:** A formal cloud-based CI/CD pipeline is deferred for post-MVP.
*   **Database Choice & Data Modeling:** Not required for MVP; current file logging in `data/` is sufficient.
*   **Authentication & Authorization:** Not required for MVP (anonymous access).
*   **Scaling Strategy:** Defer for post-MVP; local deployment focuses on single-instance.
*   **Advanced UI/UX Frameworks:** Streamlit components are sufficient for MVP.

### External Weather API Provider

*   **Decision:** WeatherAPI.com
*   **Version:** Latest free tier API
*   **Rationale:** Chosen for its robust free tier (1,000 calls/day), provision of all required data points (Wind, Precipitation, Feels Like Temp, UV Index), and the convenience of not requiring a credit card for free tier access, making it ideal for an academic project.

### Hosting Strategy

*   **Decision:** Local Deployment, focused on ease of setup via `venv` and `requirements.txt`.
*   **Rationale:** Aligns with the project's academic context, simplifying evaluation. File I/O operations for the `data/` directory will use **Python's `pathlib` module** to ensure cross-platform compatibility (Windows/macOS) by correctly handling path separators.

### Development Methodology

*   **Agile Principles**: The development process will strictly follow Agile principles, utilizing User Stories for incremental development and clear progression.
*   **Local Continuous Integration**: Continuous Integration practices will be applied locally, with QA checks and module verification before integration to ensure each component works as expected. This approach facilitates iterative review and provides clear checkpoints on functionality and progress.

### Decision Impact Analysis

**Implementation Sequence:**
1.  Set up Python virtual environment and install dependencies from `requirements.txt`.
2.  Configure API keys in a `.env` file for WeatherAPI.com and Gemini.
3.  Implement weather data fetching and parsing using WeatherAPI.com.
4.  Implement the Heuristic Safety Engine.
5.  Integrate Gemini LLM for interpretative explanations.
6.  Develop Streamlit UI components, including the dual-output report generation (browser download and local log via `pathlib`).

**Cross-Component Dependencies:**
*   The WeatherAPI.com integration directly impacts the Heuristic Engine and LLM input.
*   The local deployment strategy dictates the use of `venv` and `requirements.txt` as core setup components.
*   File I/O operations are dependent on `pathlib` for cross-platform robustness.

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:**
Identified potential for conflicts in naming, code organization, data formats, and process handling which are addressed by the following patterns.

### Naming Patterns

**Code Naming Conventions:** All Python code (modules, functions, variables, classes) will strictly follow **PEP 8**. This means `snake_case` for functions, variables, and module names, and `CamelCase` for class names.
**API Naming Conventions (Internal Data Structures):** Internal Python data structures representing API responses or requests will be converted to and handled with `snake_case` to maintain internal consistency.
**File and Directory Naming:** Files and directories will use `snake_case` (e.g., `my_module.py`, `my_directory/`).

### Structure Patterns

**Project Organization:** The project will utilize a **By Type (Layered Architecture)** for its primary organization, promoting clear separation of concerns.
*   **`app.py`:** The main application entry point, housing the Streamlit UI code.
*   **`engine/`:** Contains the core business logic, specifically the Heuristic Safety Engine.
*   **`services/`:** For all communication with external APIs, including client implementations for WeatherAPI.com and the Gemini LLM.
*   **`data/`:** Dedicated to storing runtime-generated report logs.
*   **`assets/`:** Houses static resources such as custom CSS or images.
**File Structure Patterns:** All tests will reside in a top-level **`tests/`** directory, mirroring the application's structure for clear association (e.g., `tests/engine/test_heuristic.py`).

### Format Patterns

**API Response Formats (Internal Data):** We will **use Pydantic models for all internal data structures** (e.g., Weather data from WeatherAPI.com, Heuristic Safety Assessments, LLM outputs, final Reports). This ensures strict type validation, promotes a "fail-fast" approach to data issues, and clearly defines our data contracts.
**Error Standardization:**
*   **Model:** Implement a Pydantic-based `AppError` model for all system failures.
*   **Fields:** Every error must include a machine-readable `error_code` (string, e.g., `WEATHER_API_UNAVAILABLE`), a `user_message` (string) for general user display, and an optional `timestamp` in ISO 8601 format.
*   **Internal Flow:** We will use standard Python exceptions for internal logic, but ensure they are caught and "wrapped" into the `AppError` model before being passed to the Streamlit UI or recorded in the `data/` log.
*   **UI Pattern:** In `app.py`, we will use `st.error()` to display the `user_message` from the `AppError` object whenever a service or critical function fails.
**Date/Time Formats:**
*   **Internal Processing & Logging:** We will strictly adhere to **ISO 8601 format in UTC** (e.g., `YYYY-MM-DDTHH:MM:SSZ`) for all internal processing and file logging to avoid timezone ambiguities.
*   **User Display:** Dates and times will be converted from UTC to the user's local time format only at the Streamlit UI layer for user convenience.
**JSON Field Naming:** To handle the mismatch between external `camelCase` APIs and our internal `snake_case` Python code, we will **use Pydantic's `alias_generator` feature**.

### Communication Patterns

**State Management:** We will **use `st.session_state` to persist weather data and Gemini assessments** across Streamlit reruns, ensuring a consistent user experience.
**Logging:** We will utilize the **standard Python `logging` module** for console debugging and internal system messages. Log messages will be descriptive and provide relevant context.

### Process Patterns

**Loading States (Feedback):** To meet UX responsiveness standards, all long-running operations (specifically API calls) will be **wrapped in `st.spinner()`** to display a clear loading indicator to the user.
**Error Handling (Recovery):** We will **use the `AppError` pattern** (as defined previously) to catch exceptions from service or engine layers and display user-friendly messages via `st.error()` in the Streamlit UI.

### Enforcement Guidelines

**All AI Agents MUST:**
- Strictly adhere to all defined Naming, Structure, Format, Communication, and Process Patterns.
- Utilize Pydantic models for data validation and API response parsing.
- Implement the `AppError` model for consistent error handling throughout the application.
- Use `pathlib` for all file I/O operations to ensure cross-platform compatibility.

**Pattern Enforcement:** Patterns will be enforced through code reviews and automated checks (e.g., linting, type checking) where applicable.

**Pattern Examples:**
**(Examples will be provided during implementation as concrete code snippets.)**

## Project Structure & Boundaries

### Complete Project Directory Structure

```
.
├── .env                  # Environment variables (ignored by git)
├── .env.example          # Example environment variables for setup
├── .gitignore            # Specifies intentionally untracked files to ignore
├── README.md             # Project overview and setup instructions
├── requirements.txt      # Python dependencies for the project
├── app.py                # Main Streamlit application entry point
├── engine/               # Core business logic (Heuristic Safety Engine)
│   ├── __init__.py       # Makes 'engine' a Python package
│   ├── heuristic_engine.py # Contains the logic for safety assessments
│   └── models.py         # Pydantic models for internal engine data structures
├── services/             # External API clients and utility services
│   ├── __init__.py       # Makes 'services' a Python package
│   ├── weather_api.py    # Client for WeatherAPI.com integration
│   ├── gemini_llm.py     # Client for Gemini LLM integration
│   ├── report_generator.py # Utility to format and generate reports (JSON/TXT)
│   ├── file_logger.py    # Utility for writing reports to the local 'data/' directory
│   └── models.py         # Pydantic models for external API response parsing
├── utils/                # General purpose utilities and common models
│   ├── __init__.py       # Makes 'utils' a Python package
│   ├── app_error.py      # Pydantic-based AppError model for consistent error handling
│   ├── constants.py      # Global constants (e.g., safety thresholds)
│   └── converters.py     # Utility functions (e.g., camelCase to snake_case if manual steps needed)
├── data/                 # Runtime-generated report logs
│   └── .gitkeep          # Ensures the 'data/' directory is committed
│   └── [timestamp_report.txt/json] # Example of generated report file
└── assets/               # Static assets for the Streamlit UI
    ├── css/
    │   └── style.css     # Custom CSS for styling (if needed)
    └── img/
        └── .gitkeep      # Ensures the 'img/' directory is committed
```

### Architectural Boundaries

**API Boundaries:**
*   **External API Endpoints**: Defined by WeatherAPI.com (HTTP GET for current/forecast weather) and Gemini LLM (HTTP POST for text generation). These are consumed via clients in `services/weather_api.py` and `services/gemini_llm.py`.
*   **Authentication**: API keys (from `.env`) are used to authenticate with external services.
*   **Data Access Layer**: Pydantic models in `services/models.py` define the boundary for data received from external APIs.

**Component Boundaries:**
*   **Streamlit UI (`app.py`)**: Handles user input, displays results, and orchestrates calls to `engine/` and `services/`.
*   **Heuristic Engine (`engine/`)**: Encapsulates all safety assessment logic, independent of UI or external services. Receives structured data, returns assessment.
*   **Service Clients (`services/`)**: Provide clean interfaces for interacting with external systems (WeatherAPI.com, Gemini) and internal utilities (report generation, file logging).
*   **Utility Modules (`utils/`)**: Provide common functionality and shared models (`AppError`) used across different layers.

**Data Boundaries:**
*   **Input Data**: User-provided location and date from `app.py`.
*   **External Data**: Weather data from WeatherAPI.com, LLM interpretations from Gemini. These are validated and structured by Pydantic models in `services/models.py`.
*   **Internal Data**: Pydantic models in `engine/models.py` and `utils/app_error.py` define the structure of data within the application (e.g., `WeatherReport`, `SafetyAssessment`, `AppError`).
*   **Persistent Data**: Generated reports in JSON/TXT format are written to the `data/` directory.

### Requirements to Structure Mapping

**Functional Requirements:**
*   **User Input (FR2, FR3)**: Handled in `app.py` using Streamlit widgets.
*   **Fetch Weather Data (FR4)**: Implemented in `services/weather_api.py`.
*   **Safety Assessment (FR5, FR9)**: Core logic resides in `engine/heuristic_engine.py`.
*   **LLM Explanation (FR6)**: Implemented in `services/gemini_llm.py`.
*   **Display UI/Results (FR7, FR8)**: Handled in `app.py`.
*   **API Error Handling (FR10, FR11, FR12)**: Implemented within `services/` clients and caught/displayed via `AppError` in `app.py`.
*   **Generate Report (FR13, FR14)**: `services/report_generator.py` for formatting, `services/file_logger.py` for local logging, `app.py` for UI download button.

**Cross-Cutting Concerns:**
*   **Security (NFR4, NFR5)**: API keys in `.env` (root), input sanitization within `app.py` and Pydantic models.
*   **Maintainability (NFR6, NFR7, NFR8)**: `requirements.txt` (root), PEP 8 (global adherence), modular structure (all components).
*   **Compatibility (NFR10, NFR11)**: `pathlib` for file I/O (implemented in `services/file_logger.py`).

### Integration Points

**Internal Communication:**
*   `app.py` orchestrates calls to `engine/` for logic and `services/` for external interactions and utilities.
*   Data passed between these components will primarily use Pydantic models, ensuring type safety and consistency.
*   `st.session_state` (managed in `app.py`) for persisting data across Streamlit reruns.

**External Integrations:**
*   **WeatherAPI.com**: Via `services/weather_api.py`.
*   **Gemini LLM**: Via `services/gemini_llm.py`.

**Data Flow:**
User Input (`app.py`) -> WeatherAPI.com (`services/weather_api.py`) -> Raw Weather Data (Pydantic model) -> Heuristic Engine (`engine/heuristic_engine.py`) -> Safety Assessment (Pydantic model) -> Gemini LLM (`services/gemini_llm.py`) -> AI Explanation -> Display (`app.py`) & Log (`services/file_logger.py`) & Download (`app.py`).

### File Organization Patterns

**Configuration Files:**
*   `.env`, `.env.example`, `requirements.txt`, `.gitignore` in the project root.
**Source Organization:**
*   Categorized by type (`engine/`, `services/`, `utils/`) for clear separation of concerns.
**Test Organization:**
*   A dedicated top-level `tests/` directory, mirroring the source code structure for corresponding tests.
**Asset Organization:**
*   `assets/` for static files, with subdirectories for `css/` and `img/`.

### Development Workflow Integration

The project structure is designed to support the local Agile and Continuous Integration development methodology by providing clear module boundaries and dedicated test locations, enabling incremental development and verified integration of each component.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** All technology choices (Python, Streamlit, Pydantic, WeatherAPI.com) and development patterns are fully compatible.
**Pattern Consistency:** The defined patterns for naming, structure, and data formats are internally consistent and align with Python and Streamlit best practices.
**Structure Alignment:** The project structure directly supports the layered architecture, modularity, and testing strategy.

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:** All functional requirements from the PRD, from user input to file operations, have been mapped to a specific component in the architecture.
**Non-Functional Requirements Coverage:** All NFRs, including performance, security, maintainability, and compatibility, have been addressed through specific architectural decisions and patterns (e.g., Streamlit caching, `.env` files, PEP 8, `pathlib`).

### Implementation Readiness Validation ✅

**Decision Completeness:** All critical decisions have been documented with clear rationale and versions where applicable.
**Structure Completeness:** The project directory structure is comprehensive and provides a clear home for all components of the MVP.
**Pattern Completeness:** All major categories of implementation patterns (Naming, Structure, Format, Communication, Process) have been defined to ensure agent consistency.

### Gap Analysis Results

**Critical Gaps:** None identified. The architecture is ready for implementation.
**Important Gaps (To be addressed during implementation):**
*   **Domain Logic - Safety Thresholds**: The specific numerical values for safety thresholds (e.g., wind speed, UV index levels) need to be defined as constants during implementation.
*   **AI - Prompt Engineering**: The exact prompts to be sent to the Gemini LLM for generating explanations will be developed and refined during the implementation of the `services/gemini_llm.py` client.

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Development methodology defined

**✅ Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** High
**Key Strengths:**
*   **Simplicity & Focus:** The architecture is lean and directly serves the MVP requirements without over-engineering.
*   **Clarity & Consistency:** The defined patterns and layered structure provide a clear, unambiguous guide for implementation.
*   **Robustness:** The use of Pydantic for data validation and a dedicated `AppError` model will significantly improve the application's reliability.

**Areas for Future Enhancement:**
*   **CI/CD Pipeline:** Integration of a formal CI/CD pipeline for automated testing and deployment.
*   **Database Integration:** If future requirements call for persistent user data or historical trend analysis, a database would be a necessary addition.

### Implementation Handoff

**AI Agent Guidelines:**
*   Follow all architectural decisions exactly as documented.
*   Use implementation patterns consistently across all components.
*   Respect the defined project structure and component boundaries.
*   Refer to this document for all architectural questions.

**First Implementation Priority:**
*   Set up the project structure and local environment as defined in the "Starter Template Evaluation" section (create folders, `venv`, `requirements.txt`, `.env.example`).