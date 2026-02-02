from services.report_generator import generate_report
from services.lean_weather_models import LeanWeatherApiResponse  # FIX: Use Lean model
from services.models import GeminiOutput
from engine.models import HeuristicOutput

def test_generate_report_assembles_data_correctly():
    """
    Tests that the generate_report function correctly assembles all input
    data into a comprehensive AssessmentReport object. (Story 5.1)
    """
    # 1. Arrange: Create mock input data
    mock_location_name = "Test City"
    mock_assessment_date = "2026-01-26"

    # FIX: Use LeanWeatherApiResponse instead of WeatherApiResponse
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

    mock_heuristic_output = HeuristicOutput(
        decision="GO",
        reasons=["Conditions are favorable"],
        weighted_score=95.0,
        notes="Conditions look great for an outing."
    )

    mock_ai_explanation = GeminiOutput(
        explanation="It's a great day for an outing!"
    )

    # 2. Act: Call the function we are testing
    report = generate_report(
        location_name=mock_location_name,
        assessment_date=mock_assessment_date,
        weather_data=mock_weather_data,
        heuristic_output=mock_heuristic_output,
        ai_explanation=mock_ai_explanation
    )

    # 3. Assert: Check that all data is present in the report
    assert report.location_name == mock_location_name
    assert report.assessment_date == mock_assessment_date
    assert report.weather_data == mock_weather_data
    assert report.heuristic_output == mock_heuristic_output
    assert report.ai_explanation == mock_ai_explanation