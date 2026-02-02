import json
import pytest
from services.file_logger import log_report_to_file
from services.models import AssessmentReport, GeminiOutput
from services.lean_weather_models import LeanWeatherApiResponse  # FIX: Use Lean model
from engine.models import HeuristicOutput

@pytest.fixture
def mock_report():
    """Creates a reusable mock AssessmentReport for tests."""
    # This code now belongs INSIDE the function
    mock_weather_dict = {
        "location": {"name": "Testville", "region": "Test Region", "country": "Testland"},
        "current": {"temp_c": 10.0, "wind_mph": 5.0, "precip_mm": 0.0, "uv": 3, "feelslike_c": 9.0},
        "forecast": {"forecastday": [{"date": "2026-01-27", "day": {"daily_chance_of_rain": 20}, "astro": {}, "hour": []}]}
    }
    valid_weather_data = WeatherApiResponse.model_validate(mock_weather_dict)

    return AssessmentReport(
        report_id="rep_test123",
        location_name="Testville",
        assessment_date="2026-01-27",
        # This is the crucial change: use the variable from above
        weather_data=valid_weather_data,
        heuristic_output=HeuristicOutput(decision="GO", reasons=[], weighted_score=100.0, notes="Perfect weather noted."),
        ai_explanation=GeminiOutput(explanation="Looks good.")
    )

def test_log_report_to_file_appends_to_json(tmp_path, monkeypatch):
    """Test that log_report_to_file creates/appends to a JSON file."""
    log_file = tmp_path / "test_logs.json"
    
    # FIX: Use LeanWeatherApiResponse and add maxtemp_c, mintemp_c
    mock_weather_dict = {
        "location": {"name": "Test City", "region": "Test Region", "country": "Testland"},
        "current": {"temp_c": 10.0, "wind_mph": 5.0, "precip_mm": 0.0, "uv": 3.0, "feelslike_c": 9.0},
        "forecast": {"forecastday": [{
            "date": "2026-01-26",
            "day": {
                "daily_chance_of_rain": 20,
                "maxtemp_c": 15.0,
                "mintemp_c": 5.0
            }
        }]}
    }
    mock_weather_data = LeanWeatherApiResponse.model_validate(mock_weather_dict)
    
    # FIX: Create a proper AssessmentReport
    from services.models import AssessmentReport
    
    mock_report = AssessmentReport(
        location_name="Test City",
        assessment_date="2026-01-26",
        weather_data=mock_weather_data,
        heuristic_output=HeuristicOutput(
            decision="GO",
            reasons=["Good weather"],
            weighted_score=95.0,
            notes="Test notes"
        ),
        ai_explanation=GeminiOutput(explanation="Test explanation")
    )
    
    # Arrange: Point the logger to a temporary file
    # FIX: Pass Path object, not string, and also patch DATA_DIR
    monkeypatch.setattr('services.file_logger.LOG_FILE', log_file)
    monkeypatch.setattr('services.file_logger.DATA_DIR', tmp_path)
    
    # Act: Log the report
    log_report_to_file(mock_report)
    
    # Assert: Check if the file was created and has one entry
    assert log_file.exists()
    with log_file.open('r') as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]['location_name'] == "Test City"