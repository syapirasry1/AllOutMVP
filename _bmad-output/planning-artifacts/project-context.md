# Project Context: AllOut

_This document provides a comprehensive, AI-native guide to the "AllOut" project. It synthesizes the Product Requirements Document (PRD) and the Architecture Decision Document (ADD) into a single source of truth for implementation._

## 1. Project Goal & Vision

**Core Problem:** Standard weather apps provide raw data but fail to interpret what it means for user safety and comfort. This "interpretation gap" can lead to poor decisions, from ruined picnics to serious safety incidents.

**Our Solution ("AllOut"):** An AI-powered decision-support tool that analyzes environmental data (Wind, Precipitation, Feels Like Temp, UV Index) and provides a clear, actionable "Go/No-Go" assessment. It delivers not just the 'what' (data) but the 'so what' (its direct impact).

**Primary Innovation:**
- **AI-driven Interpretation:** Uses Gemini to translate complex data into plain-language explanations.
- **Challenges "Rain-Centric" Bias:** Prioritizes "invisible" risks like high UV index and wind gusts.
- **Assumes No Data Literacy:** Acts as a translation layer between raw data and user-friendly advice.

## 2. Target Users

- **Adhit (The Adventurer):** A serious hiker who needs reliable, nuanced safety information for potentially hazardous environments (e.g., mountain ridges). For him, AllOut is a critical pre-flight safety check.
- **Sisi (The Casual User):** A parent planning everyday outdoor activities (e.g., park picnics). For her, AllOut is a "Safety Buddy" that provides reassurance and prevents discomfort.

## 3. Core Functional Requirements

- **Anonymous Access:** No login required.
- **User Input:** User provides a geographical location and a date.
- **Heuristic Engine:** A deterministic, rule-based engine provides a primary safety status (Green, Amber, Red). **This engine's decision is final and cannot be overridden by the AI.**
- **AI Explanation:** An LLM (Gemini 2.5 Flash) generates a conversational explanation of the heuristic status.
- **Error Handling:** The system must gracefully handle external API timeouts, partial data, and unexpected schema changes with specific user-facing messages.
- **Report Generation:** The user can download a summary report (`.txt` or `.json`) containing raw metrics, the heuristic status, and the AI interpretation. A copy of every report is also saved to a local `./data/` directory for audit purposes.

## 4. Technology Stack & Architecture

- **Language/Runtime:** **Python 3.x**
- **Web Framework:** **Streamlit**. Chosen for rapid development of data-centric apps.
- **Dependency Management:** `requirements.txt`
- **Testing Framework:** `pytest` for all business logic, helpers, and the heuristic engine.
- **Key Libraries & Modules:**
    - **`pathlib`:** **MUST** be used for all file I/O to ensure cross-platform (Windows/macOS) compatibility.
    - **Pydantic:** **MUST** be used for all internal data structures, API responses, and error models to ensure strict type validation.
    - **`st.session_state`:** Used to persist data across Streamlit UI reruns.
    - **Standard `logging` module:** For console debugging.
    - **`.env` files:** For secure management of API keys (WeatherAPI.com, Gemini).

## 5. Project Structure

The project **MUST** follow this layered structure:

```
.
├── .env
├── .env.example
├── README.md
├── requirements.txt
├── app.py                # Main Streamlit UI entry point
├── engine/               # Core Heuristic Safety Engine logic
│   ├── heuristic_engine.py
│   └── models.py         # Pydantic models for engine data
├── services/             # External API clients and utilities
│   ├── weather_api.py    # Client for WeatherAPI.com
│   ├── gemini_llm.py     # Client for Gemini LLM
│   ├── report_generator.py
│   ├── file_logger.py    # Writes reports to the local 'data/' directory
│   └── models.py         # Pydantic models for external API data
├── utils/                # Shared utilities
│   ├── app_error.py      # Pydantic-based AppError model
│   ├── constants.py      # Safety thresholds, etc.
│   └── converters.py     # Data conversion utilities
├── data/                 # Runtime-generated report logs
└── assets/               # Custom CSS, images
```

## 6. CRITICAL Implementation Patterns & Rules

**AI Agents MUST strictly adhere to these rules.**

1.  **Naming:**
    - **Python Code:** `snake_case` for functions, variables, modules. `CamelCase` for classes (PEP 8).
    - **Files/Directories:** `snake_case`.

2.  **Data Formats & Validation:**
    - **Pydantic is Mandatory:** Use Pydantic models for all data structures (API responses, internal logic, errors). This is non-negotiable.
    - **API Field Naming:** Use Pydantic's `alias_generator` to convert external `camelCase` JSON fields to internal `snake_case`.
    - **Error Handling Model:** Implement and use a Pydantic-based `AppError` model for all system failures (`error_code`, `user_message`, `timestamp`). Wrap standard exceptions into this model before passing to the UI.
    - **Date/Time:** Use **ISO 8601 format in UTC** (`YYYY-MM-DDTHH:MM:SSZ`) for all internal processing and logging.

3.  **Process & UI Feedback:**
    - **Loading States:** All long-running operations (API calls) **MUST** be wrapped in `st.spinner()` to provide user feedback.
    - **Error Display:** Use `st.error()` to display the `user_message` from the caught `AppError` object.

4.  **File Operations:**
    - **Cross-Platform Paths:** **MUST** use Python's `pathlib` module for all file and path manipulation to ensure Windows/macOS compatibility.

## 7. First Implementation Step

The first priority is to **scaffold the project structure** as defined in Section 5. This includes creating all directories and empty `__init__.py` files, `app.py`, and other initial files (`.env.example`, `requirements.txt`).
