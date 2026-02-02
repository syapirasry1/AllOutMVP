import os
import requests
from dotenv import load_dotenv
from pydantic import ValidationError

# FIX: Import the new lean model instead of the old one
from .lean_weather_models import LeanWeatherApiResponse
from utils.app_error import AppErrorWrapper


class WeatherApiClient:
    BASE_URL = "http://api.weatherapi.com/v1"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHERAPI_KEY")
        if not self.api_key:
            raise AppErrorWrapper(
                error_code="WEATHERAPI_KEY_MISSING",
                user_message="WeatherAPI key is not configured. Please set WEATHERAPI_KEY in your .env file."
            )

    def get_weather_data(self, location: str, date: str = None) -> LeanWeatherApiResponse: # FIX: Update the return type hint
        """
        Fetches weather data from the WeatherAPI.
        Extracts current weather from the first hour of the forecast.
        """
        params = {
            "key": self.api_key,
            "q": location,
            "days": 1,
            "aqi": "no"
        }
        if date:
            params["dt"] = date

        try:
            response = requests.get(f"{self.BASE_URL}/forecast.json", params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # FIX: Remove the debug print block
            # === DEBUG: Print the actual response ===
            # print("\n" + "="*80)
            # print("DEBUG: Full Response JSON:")
            # print("="*80)
            # import json
            # print(json.dumps(data, indent=2))
            # print("="*80 + "\n")
            # === END DEBUG ===

            if not data.get("forecast", {}).get("forecastday"):
                raise AppErrorWrapper(
                    error_code="WEATHERAPI_NO_FORECAST_FOR_DATE",
                    user_message="No forecast data available for the selected date."
                )

            # FIX: No changes needed here. Your logic for building the 'current' object is good.
            # We will let Pydantic handle the parsing from the full 'data' object.
            forecast_day = data["forecast"]["forecastday"][0]
            first_hour = forecast_day["hour"][0] if forecast_day.get("hour") else {}
            
            current_data = {
                "temp_c": first_hour.get("temp_c", 0),
                "feelslike_c": first_hour.get("feelslike_c", 0),
                "wind_mph": first_hour.get("wind_mph", 0),
                "precip_mm": first_hour.get("precip_mm", 0),
                "uv": first_hour.get("uv", 0),
            }
            
            data["current"] = current_data

            # FIX: Use the lean model for parsing. Pydantic will automatically
            # ignore all the extra fields we don't need.
            return LeanWeatherApiResponse.parse_obj(data)

        except requests.exceptions.Timeout:
            raise AppErrorWrapper(
                error_code="WEATHERAPI_TIMEOUT",
                user_message="The request to the weather service timed out."
            )
        except requests.exceptions.ConnectionError:
            raise AppErrorWrapper(
                error_code="WEATHERAPI_CONNECTION_ERROR",
                user_message="Could not connect to the weather service."
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AppErrorWrapper(
                    error_code="WEATHERAPI_AUTH_FAILED",
                    user_message="Authentication with the weather service failed. Check your API key."
                ) from e
            elif e.response.status_code == 403:
                raise AppErrorWrapper(
                    error_code="WEATHERAPI_FORBIDDEN",
                    user_message="Access to the requested weather resource is forbidden."
                ) from e
            elif e.response.status_code == 400:
                error_data = e.response.json().get("error", {})
                raise AppErrorWrapper(
                    error_code=f"WEATHERAPI_BAD_REQUEST_{error_data.get('code', 'UNKNOWN')}",
                    user_message=f"Bad request to weather service: {error_data.get('message', 'Unknown error')}"
                ) from e
            else:
                raise AppErrorWrapper(
                    error_code="WEATHERAPI_UNKNOWN_ERROR",
                    user_message=f"An unexpected error occurred with the weather service: {e.response.status_code}"
                ) from e
        except ValidationError as e:
            missing_fields = [str(error['loc'][0]) for error in e.errors() if error['type'] == 'missing']
            raise AppErrorWrapper(
                error_code="WEATHERAPI_SCHEMA_CHANGE_MISSING_FIELDS",
                user_message=f"Missing or invalid fields in weather data: {', '.join(missing_fields)}"
            ) from e
        except AppErrorWrapper as e:
            raise e
        except Exception as e:
            raise AppErrorWrapper(
                error_code="WEATHERAPI_UNEXPECTED_ERROR",
                user_message=f"An unexpected error occurred: {str(e)}"
            ) from e

    def get_weather(self, location, date):
        """Wrapper method for compatibility."""
        return self.get_weather_data(location, date)