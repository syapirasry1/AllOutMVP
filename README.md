# AllOut - Outdoor Safety Assessment System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Tests](https://img.shields.io/badge/tests-37%20passing-success.svg)
![Version](https://img.shields.io/badge/version-3.7.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 Project Description

**AllOut** is an intelligent outdoor safety assessment application that helps outdoor enthusiasts make informed go/no-go decisions for their planned activities. By combining real-time weather data with rule-based safety heuristics and AI-powered explanations, AllOut provides clear, actionable safety recommendations.

The system evaluates weather conditions (wind, temperature, probability of precipitation, precipitation amount, and UV index) against established safety thresholds and delivers a simple **GO**, **MAYBE**, or **NO-GO** decision, accompanied by detailed explanations and practical recommendations.

---

## 🎯 Problem Statement & Target Users

### Problem Solved
Outdoor enthusiasts often struggle to:
- Interpret complex weather data for safety implications
- Understand the cumulative risk of multiple weather factors
- Make quick, informed decisions about outdoor activity safety
- Get practical, actionable advice beyond raw weather forecasts

### Intended Users
- **Hikers & Trekkers** planning day trips or multi-day expeditions
- **Outdoor Activity Organizers/Business** coordinating group events
- **Trail Runners & Cyclists** assessing conditions for training
- **Casual Outdoor Enthusiasts** seeking safety guidance for picnics, camping, or outdoor sports

---

### How AllOut Makes Decisions

**AllOut uses its own custom-built rule-based engine to aggregate and assess weather conditions**. This engine applies transparent, pre-defined safety thresholds and weights to each weather metric (wind, temperature, precipitation, UV, etc.) to calculate a safety score and make a clear **GO / MAYBE / NO-GO** decision. 

The AI (Gemini) is then used **only to explain and contextualize** this decision for the user, never to override or contradict the engine’s assessment. This ensures that every safety recommendation is consistent, explainable, and based on established safety logic—not just an AI’s opinion.

---

## ✨ Key Functionalities

### 1. **Intelligent Safety Assessment**
- **Rule-Based Heuristic Engine**: Evaluates weather metrics against safety thresholds
- **Weighted Scoring System**: Combines wind (20%), thermal stress (35%), precipitation (40%), and UV (5%)
- **Hard-Stop Rules**: Immediate NO-GO for extreme conditions (wind ≥32 mph, extreme heat/cold, heavy rain)

### 2. **Visual Safety Indicators**
- **Color-Coded Decisions**:
  - ✅ **GO** (Green): Safe conditions, score ≥75/100
  - ⚠️ **MAYBE** (Amber): Marginal conditions, score 50-74/100
  - 🛑 **NO-GO** (Red): Unsafe conditions, score <50/100 or hard-stop triggered
- **Large, Prominent Display**: Easy-to-read decision boxes with emoji indicators

### 3. **AI-Powered Explanations**
- **Google Gemini 2.5 Flash Integration**: Generates conversational explanations
- **Structured Recommendations**:
  - Weather Summary
  - Specific Clothing Advice
  - 2 Practical Non-Clothing Tips (safety + activity planning)
- **Context-Aware**: Tailored advice based on GO/MAYBE/NO-GO decision

### 4. **Comprehensive Weather Data**
- **Real-Time Data**: Current weather conditions via WeatherAPI.com
- **5 Key Metrics**: Wind speed, feels-like temperature, UV index, rain chance, precipitation amount
- **Forecast Data**: Daily chance of rain for activity planning

### 5. **Report Export & Logging**
- **JSON Export**: Machine-readable format for data processing
- **TXT Export**: Human-readable summary for easy reading
- **Persistent Logging**: All assessments logged to `data/assessment_logs.json` with ISO 8601 UTC timestamps

---

## 🚀 How to Run the Code

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- API Keys:
  - [WeatherAPI.com](https://www.weatherapi.com/) (free tier)
  - [Google AI Studio](https://aistudio.google.com/) for Gemini API (free tier)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AllOut.git
   cd AllOut
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**
   
   Create a `.env` file in the project root:
   ```env
   WEATHER_API_KEY=your_weatherapi_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

1. **Start the Streamlit App**
   ```bash
   streamlit run app.py
   ```

2. **Access the App**
   - Open your browser to `http://localhost:8501`
   - Enter a location (e.g., "Coventry", "New York")
   - Select an assessment date
   - Click "Assess Safety"

3. **Run Tests**
   ```bash
   pytest tests/ -v
   ```
   Expected: 37/37 tests passing ✅

---

## 🤖 AI Tools Used

### 1. **Google Gemini 2.5 Flash (Primary AI)**
- **Purpose**: Generate conversational safety explanations for users
- **Role**: 
  - Interprets weather data and heuristic decisions
  - Provides context-aware recommendations
  - Generates structured output with clothing and practical tips
- **Integration**: `services/gemini_llm.py`
- **Prompt Engineering**: Structured prompts ensuring alignment with heuristic decisions

### 2. **Gemini-CLI & BMAD (Planning & Analysis)**
- **Purpose**: Advanced planning, requirements analysis, architecture design, and early development
- **Role**:
  - Used different agents (analyst, PM, architect, SM, developer) to simulate collaborative planning and decision-making
  - Supported backlog creation, story mapping, and architecture documentation
  - Helped setting up the first code of AllOut 
- **Impact**: Improved project structure, ensured thorough analysis, and supported agile, iterative development

### 3. **Google Gemini (General Development Support)**
- **Purpose**: Assisted in every phase of development
- **Role**:
  - Provided quick answers to technical questions and unknown terms
  - Helped debug and troubleshoot issues, especially with Gemini LLM integration
  - Helped clarify unknown terms, balance pros and cons of choices
  - Aided in balancing trade-offs and making informed decisions during planning and implementation

### 4. **Claude Sonnet 4.5 (Development Assistant)**
- **Purpose**: Code development and architecture design
- **Role**:
  - Implemented core business logic (heuristic engine)
  - Designed service layer architecture
  - Created comprehensive test suite
  - Developed error handling patterns
- **Impact**: Accelerated development with clean, maintainable code

### 5. **GitHub Copilot (Code Completion)**
- **Purpose**: Code suggestions and  generation
- **Role**:
  - Auto-completion for repetitive code patterns
  - Test case generation
  - Documentation snippets
- **Impact**: Improved development velocity by ~30%

### 6. **Google Gemini 2.5 Pro (Code Completion)**
- **Purpose**: Assisted in error fixing and debugging during development
- **Role**:
  - Used within VSCode to quickly identify, explain, and resolve code errors
  - Provided suggestions for debugging strategies and code improvements
  - Worked in tandem with Claude Sonnet for deeper architectural and logic troubleshooting
- **Impact**: Enhanced development efficiency and code reliability through real-time AI support in the IDE

### AI Usage Summary
- **Gemini**: Production feature (user-facing AI explanations)
- **Gemini-CLI & BMAD**: Planning, analysis, and architecture support
- **Claude & Copilot**: Development tools (code generation, architecture)
- **Human Oversight**: All AI outputs reviewed and validated
- **Testing**: 37 unit tests ensure AI integration reliability

---

## 📂 Project Structure

```
AllOut/
├── app.py                      # Main Streamlit application
├── engine/                     # Core business logic
│   ├── heuristic_engine.py    # Safety assessment engine
│   └── models.py              # Domain models (HeuristicInput/Output)
├── services/                   # External service integrations
│   ├── weather_api.py         # WeatherAPI.com client
│   ├── gemini_llm.py          # Google Gemini client
│   ├── report_generator.py   # Report assembly
│   ├── file_logger.py         # Persistent logging
│   └── models.py              # Service data models
├── utils/                      # Utility functions
│   ├── app_error.py           # Custom error handling
│   └── validation.py          # Input validation
├── tests/                      # Comprehensive test suite (37 tests)
├── data/                       # Log files (assessment_logs.json)
├── .env                        # API keys (not in repo)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🏗️ Architecture Highlights

### Design Patterns
- **Service Layer Pattern**: Clear separation between UI, business logic, and external services
- **Repository Pattern**: File-based logging with clean abstraction
- **Error Wrapper Pattern**: Consistent error handling across all layers

### Key Technologies
- **Streamlit**: Interactive web UI framework
- **Pydantic**: Data validation and serialization
- **Pytest**: Comprehensive unit testing
- **Python Dotenv**: Secure environment variable management

### Quality Assurance
- **37 Unit Tests**: 100% passing rate
- **Error Handling**: Graceful degradation for API failures
- **Input Validation**: Sanitized user inputs
- **ISO 8601 UTC**: Standardized timestamps

---

## 📊 Version History

- **v3.7.0** (Current) - Enhanced AI explanations with structured recommendations (350-word limit)
- **v3.6.1** - Removed developer mock options for production readiness
- **v3.6.0** - Visual safety indicators with color coding
- **v3.5.0** - Report export (JSON + TXT)
- **v3.4.0** - Gemini AI integration with graceful fallback
- **v3.3.0** - Persistent file logging system
- **v3.2.0** - WeatherAPI integration
- **v3.1.0** - Report generation
- **v3.0.0** - Core heuristic engine implementation

---

## 🔗 GitHub Repository

**Repository URL**: [https://github.com/yourusername/AllOut](https://github.com/yourusername/AllOut)

**View Version History**:
- [Releases](https://github.com/yourusername/AllOut/releases) - All tagged versions
- [Commits](https://github.com/yourusername/AllOut/commits/main) - Full development history
- [Issues](https://github.com/yourusername/AllOut/issues) - Bug tracking and feature requests

---

## 📝 Documentation

Comprehensive documentation available in `_bmad-output/`:
- **Planning Artifacts**: PRD, architecture, project backlog
- **Implementation Artifacts**: Story-by-story implementation details
- **Architecture Document**: System design and patterns
- **Project Context**: Development methodology and guardrails

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/engine/ -v           # Heuristic engine tests
pytest tests/services/ -v         # Service layer tests

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Coverage**: 37 tests covering:
- Heuristic engine logic (12 tests)
- Weather API client (10 tests)
- Gemini LLM client (10 tests)
- Report generation (3 tests)
- UI validation (2 tests)

---

## 🛡️ Error Handling

AllOut implements comprehensive error handling:
- **API Failures**: Graceful degradation with user-friendly messages
- **Rate Limiting**: 429 error fallback with general safety advice
- **Timeouts**: 6-second timeout with retry guidance
- **Invalid Inputs**: Input sanitization and validation
- **Missing Data**: Clear messaging for insufficient data scenarios

---

### Limitations & Agile Roadmap

I acknowledge that the current engine calculation, while robust for an MVP, lacks nuance and does not capture the full complexity of weather assessment. Weather safety depends on many more factors than the five metrics currently used (wind, temperature, precipitation, rain chance, and UV index). As part of an agile, iterative development process, I plan to enhance AllOut by incorporating additional weather variables, more sophisticated risk models, and user feedback in future releases. This approach ensures continuous improvement and responsiveness to real-world needs.

---

## 🌟 Future Enhancements

- [ ] Expanded weather metrics (e.g., visibility, cloud cover)
- [ ] User profiles with activity-specific thresholds and advanced personalization
- [ ] Historical weather comparison and trend analysis
- [ ] Mobile-responsive design improvements and potential native mobile app
- [ ] Email report delivery and proactive notifications
- [ ] Integration with fitness tracking apps and third-party platforms via API
- [ ] Community integration for sharing plans and real-time conditions
- [ ] Advanced analytics for commercial outdoor activity operators

---