from pydantic import BaseModel, Field
from typing import List, Optional

# This is the input model for the engine, now with Optional fields
class HeuristicInput(BaseModel):
    temp_c: float
    feelslike_c: float
    wind_mph: Optional[float] = None  # FIX: Make Optional
    precip_mm: float
    uv_index: Optional[float] = None  # FIX: Make Optional
    daily_chance_of_rain: int
    heat_index_c: Optional[float] = None  # FIX: Make Optional
    wind_chill_c: Optional[float] = None
    pop_percent: Optional[int] = None  # FIX: Make Optional
    precip_rate_mmhr: Optional[float] = None  # FIX: Make Optional

# This is the output model for the engine
class HeuristicOutput(BaseModel):
    decision: str
    notes: str
    weighted_score: Optional[float] = None
    hard_stop_reasons: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)