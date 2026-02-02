from pydantic import BaseModel
from typing import List

# FIX: Define Location here instead of importing it
class Location(BaseModel):
    name: str
    region: str
    country: str

class LeanCurrent(BaseModel):
    temp_c: float
    feelslike_c: float
    wind_mph: float
    precip_mm: float
    uv: float

class LeanDay(BaseModel):
    maxtemp_c: float
    mintemp_c: float
    daily_chance_of_rain: int

class LeanForecastDay(BaseModel):
    date: str
    day: LeanDay

class LeanForecast(BaseModel):
    forecastday: List[LeanForecastDay]

class LeanWeatherApiResponse(BaseModel):
    location: Location
    current: LeanCurrent
    forecast: LeanForecast