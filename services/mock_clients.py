"""
Mock clients for development and testing purposes.
These clients mimic the real API clients but return hardcoded data
without making any actual network requests.
"""
from .models import (
    WeatherApiResponse, Location, Current, Day, Forecast, ForecastDay,
    GeminiOutput
)

class MockWeatherApiClient:
    """
    A mock version of the WeatherApiClient that returns different data
    based on the location input to simulate different scenarios.
    """
    def get_weather_data(self, location: str, date: str) -> WeatherApiResponse:
        
        location_lower = location.lower()

        # --- Scenario 1: NO-GO (for Jakarta) ---
        # Extreme wind speed (45mph) triggers a hard stop.
        if "jakarta" in location_lower:
            print("--- Using MockWeatherApiClient: Returning 'NO-GO' data for Jakarta. ---")
            return WeatherApiResponse(
                location=Location(name="Jakarta", region="DKI Jakarta", country="Indonesia"),
                current=Current(temp_c=30.0, feelslike_c=35.0, wind_mph=45.0, precip_mm=5.0, uv=11.0),
                forecast=Forecast(forecastday=[ForecastDay(date=date, day=Day(maxtemp_c=32.0, mintemp_c=25.0, daily_chance_of_rain=70))])
            )

        # --- Scenario 2: MAYBE (for Shanghai) ---
        # High chance of rain (75%) and moderate wind, but not enough for a NO-GO.
        elif "shanghai" in location_lower:
            print("--- Using MockWeatherApiClient: Returning 'MAYBE' data for Shanghai. ---")
            return WeatherApiResponse(
                location=Location(name="Shanghai", region="Shanghai", country="China"),
                current=Current(temp_c=12.0, feelslike_c=10.0, wind_mph=15.0, precip_mm=1.0, uv=2.0),
                forecast=Forecast(forecastday=[ForecastDay(date=date, day=Day(maxtemp_c=15.0, mintemp_c=8.0, daily_chance_of_rain=75))])
            )

        # --- Scenario 3: GO (for Coventry or any other city) ---
        # Perfect, favorable conditions. This is the default case.
        else:
            print("--- Using MockWeatherApiClient: Returning 'GO' data for Coventry/Default. ---")
            return WeatherApiResponse(
                location=Location(name="Coventry", region="West Midlands", country="United Kingdom"),
                current=Current(temp_c=18.0, feelslike_c=18.0, wind_mph=5.0, precip_mm=0.0, uv=4.0),
                forecast=Forecast(forecastday=[ForecastDay(date=date, day=Day(maxtemp_c=20.0, mintemp_c=12.0, daily_chance_of_rain=10))])
            )


class MockGeminiLLMClient:
    """A mock version of the GeminiLLMClient."""
    def get_explanation(self, gemini_input) -> GeminiOutput:
        print("--- Using MockGeminiLLMClient: Returning fake AI explanation. ---")
        decision = gemini_input.heuristic_output.decision
        return GeminiOutput(
            explanation=f"This is a mock AI explanation based on simulated data. The safety decision is '{decision}' because conditions are simulated for this city. Always proceed with mock caution."
        )