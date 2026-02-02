# tests/services/test_weather_api.py

import pytest
import requests_mock
import os
from dotenv import load_dotenv
import requests.exceptions

from services.weather_api import WeatherApiClient
from services.models import WeatherApiResponse
from services.lean_weather_models import LeanWeatherApiResponse  # FIX: Add this import
from utils.app_error import AppErrorWrapper

# --- Fixtures ---
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Ensure .env is loaded and API key is present for tests."""
    monkeypatch.setenv("WEATHERAPI_KEY", "dummy_api_key")

@pytest.fixture
def weather_api_client():
    """Fixture to provide a WeatherApiClient instance."""
    return WeatherApiClient()

@pytest.fixture
def mock_weather_api(requests_mock):
    """Fixture to mock WeatherAPI.com requests."""
    return requests_mock

# --- Sample Responses (CORRECTED) ---
# CORRECTED: Added 'hour' array to provide data for the reconstructed 'current' object.
SAMPLE_CURRENT_WEATHER_RESPONSE = {
    "location": {"name": "London", "region": "City of London", "country": "UK"},
    "forecast": {
        "forecastday": [{
            "date": "2023-01-01",
            "day": {
                "daily_chance_of_rain": 20,
                "maxtemp_c": 12.0,  # FIX: Add this
                "mintemp_c": 8.0,   # FIX: Add this
                "uv": 3.0
            },
            "hour": [{
                "temp_c": 10.0,
                "feelslike_c": 8.0,
                "wind_mph": 5.0,
                "precip_mm": 0.5,
                "uv": 3.0
            }]
        }]
    }
}

# CORRECTED: Added 'hour' array here as well.
SAMPLE_FORECAST_WEATHER_RESPONSE = {
    "location": {"name": "London", "region": "City of London", "country": "UK"},
    "forecast": {
        "forecastday": [{
            "date": "2023-01-02",
            "day": {
                "daily_chance_of_rain": 60,
                "maxtemp_c": 10.0,  # FIX: Add this
                "mintemp_c": 5.0,   # FIX: Add this
                "uv": 4.0
            },
            "hour": [{
                "temp_c": 10.0,
                "feelslike_c": 8.0,
                "wind_mph": 5.0,
                "precip_mm": 0.5,
                "uv": 3.0
            }]
        }]
    }
}

SAMPLE_ERROR_RESPONSE_401 = {"error": {"code": 1002, "message": "API key not provided."}}
SAMPLE_ERROR_RESPONSE_400 = {"error": {"code": 1003, "message": "Parameter q is missing."}}

# --- Test Cases ---

def test_weather_api_key_missing_error(monkeypatch):
    """Test that AppErrorWrapper is raised if API key is missing."""
    monkeypatch.setattr('os.getenv', lambda key: None if key == "WEATHERAPI_KEY" else os.environ.get(key))
    with pytest.raises(AppErrorWrapper) as excinfo:
        WeatherApiClient()
    assert excinfo.value.error_code == "WEATHERAPI_KEY_MISSING"

def test_get_current_weather_success(weather_api_client, mock_weather_api):
    """Test successful fetching of current weather data."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        json=SAMPLE_CURRENT_WEATHER_RESPONSE
    )
    data = weather_api_client.get_weather_data(location="London")
    
    # FIX: Check for LeanWeatherApiResponse instead of WeatherApiResponse
    assert isinstance(data, LeanWeatherApiResponse)
    assert data.location.name == "London"
    assert data.current.temp_c == 10.0
    assert data.current.wind_mph == 5.0
    assert data.current.precip_mm == 0.5
    assert data.current.uv == 3.0


def test_get_forecast_weather_success(weather_api_client, mock_weather_api):
    """Test successful fetching of forecast weather data for a specific date."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        json=SAMPLE_FORECAST_WEATHER_RESPONSE
    )
    data = weather_api_client.get_weather_data(location="London", date="2023-01-02")
    
    # FIX: Check for LeanWeatherApiResponse instead of WeatherApiResponse
    assert isinstance(data, LeanWeatherApiResponse)
    assert data.location.name == "London"
    assert data.current.temp_c == 10.0
    assert data.current.wind_mph == 5.0
    assert data.current.precip_mm == 0.5
    assert data.current.uv == 3.0
    # FIX: Check forecast data structure
    assert len(data.forecast.forecastday) == 1
    assert data.forecast.forecastday[0].date == "2023-01-02"
    assert data.forecast.forecastday[0].day.daily_chance_of_rain == 60

def test_network_error(weather_api_client, mock_weather_api):
    """Test handling of network connection errors."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        exc=requests.exceptions.ConnectionError
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="London")
    assert excinfo.value.error_code == "WEATHERAPI_CONNECTION_ERROR"

def test_timeout_error(weather_api_client, mock_weather_api):
    """Test handling of request timeout errors."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        exc=requests.exceptions.Timeout
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="London")
    assert excinfo.value.error_code == "WEATHERAPI_TIMEOUT"

def test_http_401_error(weather_api_client, mock_weather_api):
    """Test handling of HTTP 401 Unauthorized error."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        status_code=401, json=SAMPLE_ERROR_RESPONSE_401
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="London")
    assert excinfo.value.error_code == "WEATHERAPI_AUTH_FAILED"

def test_http_403_error(weather_api_client, mock_weather_api):
    """Test handling of HTTP 403 Forbidden error."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        status_code=403, json={"error": {"code": 2006, "message": "API key not subscribed to this feature."}}
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="London")
    assert excinfo.value.error_code == "WEATHERAPI_FORBIDDEN"

def test_http_400_error_with_message(weather_api_client, mock_weather_api):
    """Test handling of HTTP 400 Bad Request error with specific message."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        status_code=400, json=SAMPLE_ERROR_RESPONSE_400
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="InvalidLocation")
    assert excinfo.value.error_code == "WEATHERAPI_BAD_REQUEST_1003"
    assert "Parameter q is missing" in excinfo.value.user_message

def test_http_500_error(weather_api_client, mock_weather_api):
    """Test handling of generic HTTP 500 server error."""
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        status_code=500
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="London")
    assert excinfo.value.error_code == "WEATHERAPI_UNKNOWN_ERROR"
    assert "unexpected error" in excinfo.value.user_message

def test_no_forecast_for_date_error(weather_api_client, mock_weather_api):
    """Test handling when forecast for a specific date is not returned."""
    response_no_forecast = {
        "location": {"name": "Futureland", "region": "Region", "country": "Country"},
        "current": {},
        "forecast": {
            "forecastday": [] # Empty forecastday list
        }
    }
    mock_weather_api.get(
        f"{WeatherApiClient.BASE_URL}/forecast.json",
        json=response_no_forecast
    )
    with pytest.raises(AppErrorWrapper) as excinfo:
        weather_api_client.get_weather_data(location="Futureland", date="2024-12-31")
    assert excinfo.value.error_code == "WEATHERAPI_NO_FORECAST_FOR_DATE"
    assert "No forecast data available" in excinfo.value.user_message