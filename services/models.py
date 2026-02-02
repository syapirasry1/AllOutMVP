from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from engine.models import HeuristicOutput  # Import HeuristicOutput
import uuid
from datetime import datetime, timezone
from .lean_weather_models import LeanWeatherApiResponse, Location  # FIX: Import both Location and LeanWeatherApiResponse


class Current(BaseModel):
    temp_c: float
    temp_f: float = 0.0
    feelslike_c: float
    feelslike_f: float = 0.0
    humidity: int = 0
    wind_mph: float
    wind_kph: float = 0.0
    wind_degree: int = 0
    wind_dir: str = ""
    precip_mm: float
    precip_in: float = 0.0
    condition: dict = {}
    uv: float
    is_day: int = 0
    
    # FIX: Add the missing fields. We will populate them from existing data for now.
    heat_index_c: float = Field(alias="feelslike_c")
    wind_chill_c: float = Field(alias="feelslike_c")
    
    class Config:
        extra = "allow"  # Allow extra fields from API


class Day(BaseModel):
    daily_chance_of_rain: int
    # FIX: Add the missing field. We will populate it from existing data.
    pop_percent: int = Field(alias="daily_chance_of_rain")


class ForecastDay(BaseModel):
    day: Day
    date: str


class Forecast(BaseModel):
    forecastday: List[ForecastDay]


class WeatherApiResponse(BaseModel):
    location: Location
    current: Current
    forecast: Forecast


class CurrentWeatherForGemini(BaseModel):
    temp_c: float
    feelslike_c: float
    wind_mph: float
    precip_mm: float
    uv: float


class DayForecastForGemini(BaseModel):
    daily_chance_of_rain: int
    uv: Optional[float] = None


class GeminiInput(BaseModel):
    location_name: str
    current_weather: CurrentWeatherForGemini
    day_forecast: DayForecastForGemini
    heuristic_output: HeuristicOutput


class GeminiOutput(BaseModel):
    explanation: str

    @field_validator('explanation')
    @classmethod
    def word_count_must_be_under_limit(cls, v):
        word_count = len(v.split())
        if word_count > 350:  
            raise ValueError(f"Explanation exceeds 350 words (count: {word_count})")
        return v


# NEW: Define the detailed report model as per Story 5.1
class AssessmentReport(BaseModel):
    """A comprehensive report of a single safety assessment."""
    report_id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex}")
    assessment_timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # User Inputs
    location_name: str
    assessment_date: str
    
    # Fetched Data
    # FIX: Change to LeanWeatherApiResponse
    weather_data: LeanWeatherApiResponse
    
    # Heuristic Engine Output
    heuristic_output: HeuristicOutput
    
    # AI Service Output
    ai_explanation: GeminiOutput
