from services.models import (
    AssessmentReport,
    WeatherApiResponse,
    HeuristicOutput,
    GeminiOutput
)

def generate_report(
    location_name: str,
    assessment_date: str,
    weather_data: WeatherApiResponse,
    heuristic_output: HeuristicOutput,
    ai_explanation: GeminiOutput
) -> AssessmentReport:
    """
    Assembles all inputs and outputs into a single, comprehensive AssessmentReport.
    
    This function directly implements Story 5.1.
    """
    report = AssessmentReport(
        location_name=location_name,
        assessment_date=assessment_date,
        weather_data=weather_data,
        heuristic_output=heuristic_output,
        ai_explanation=ai_explanation
    )
    return report
