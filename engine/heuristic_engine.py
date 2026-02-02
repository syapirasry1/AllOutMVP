from typing import Dict, Tuple, List, Optional
from .models import HeuristicInput, HeuristicOutput

# --- Constants for Rules ---
# Scores
GREEN_SCORE = 100.0
AMBER_SCORE = 50.0
RED_SCORE = 0.0

# Weights
WEIGHTS = {
    "wind": 0.20,
    "thermal": 0.35,
    "precip": 0.40,
    "uv": 0.05,
}

# --- Helper Functions for Categorization ---

def _categorize_wind(wind_mph: Optional[float]) -> Tuple[Optional[str], Optional[str]]:
    """Categorizes wind speed and checks for hard-stops."""
    if wind_mph is None:
        return None, None
    if wind_mph >= 32:
        return "Red", "Wind speed is at a dangerous level (>= 32 mph)."
    if wind_mph >= 20:
        return "Amber", None
    return "Green", None

def _categorize_thermal_stress(feelslike_c: Optional[float]) -> Tuple[Optional[str], Optional[str]]:
    """Categorizes thermal stress (heat/cold) and checks for hard-stops."""
    if feelslike_c is None:
        return None, None
    # Extreme Heat
    if feelslike_c >= 41:
        return "Red", "Extreme heat warning (feels like >= 41°C)."
    if feelslike_c >= 27:
        return "Amber", None
    # Extreme Cold
    if feelslike_c <= -28:
        return "Red", "Extreme cold warning (feels like <= -28°C)."
    if feelslike_c <= -10:
        return "Amber", None
    # Mild
    return "Green", None

def _categorize_precip(pop_percent: Optional[int], precip_rate_mmhr: Optional[float]) -> Tuple[Optional[str], Optional[str]]:
    """Categorizes precipitation risk and checks for hard-stops."""
    if pop_percent is None:
        return None, None
    if pop_percent <= 20:
        return "Green", None
    
    # If PoP > 20%, rate dominates
    if precip_rate_mmhr is None:
        return "Amber", None # Default to Amber if rate is unavailable but PoP is high
    if precip_rate_mmhr > 4.0:
        return "Red", "Heavy precipitation rate (> 4.0 mm/hr)."
    if precip_rate_mmhr >= 0.5:
        return "Amber", None
    return "Green", None

def _categorize_uv(uv_index: Optional[float]) -> Tuple[Optional[str], Optional[str]]:
    """Categorizes UV index."""
    if uv_index is None:
        return None, None
    if uv_index >= 8:
        return "Red", None
    if uv_index >= 3:
        return "Amber", None
    return "Green", None

# --- Main Engine ---

def run_heuristic_engine(heuristic_input: HeuristicInput) -> HeuristicOutput:
    """
    Runs the heuristic safety assessment based on weather data.
    """
    scores: Dict[str, float] = {}
    hard_stop_reasons: List[str] = []

    # 1. Categorize and check for hard-stops
    metric_map = {
        "wind": _categorize_wind(heuristic_input.wind_mph),
        "thermal": _categorize_thermal_stress(heuristic_input.heat_index_c), # Using heat_index as primary feelslike
        "precip": _categorize_precip(heuristic_input.pop_percent, heuristic_input.precip_rate_mmhr),
        "uv": _categorize_uv(heuristic_input.uv_index),
    }

    for metric, (category, reason) in metric_map.items():
        if category == "Green":
            scores[metric] = GREEN_SCORE
        elif category == "Amber":
            scores[metric] = AMBER_SCORE
        elif category == "Red":
            scores[metric] = RED_SCORE
        
        if reason:
            hard_stop_reasons.append(reason)

    # Handle no data case
    if not scores:
        return HeuristicOutput(decision="NO DATA", notes="No weather metrics were available for assessment.", weighted_score=None, reasons=[], hard_stop_reasons=[])

    # 2. Calculate weighted score (No Renormalization)
    total_score = 0.0
    for metric, score in scores.items():
        total_score += score * WEIGHTS[metric]

    # 3. Final Decision Logic
    if hard_stop_reasons:
        decision = "NO-GO"
        notes = "Assessment resulted in a NO-GO due to one or more hard-stop conditions."
    elif total_score >= 75:
        decision = "GO"
        notes = "Conditions are favorable for your activity."
    elif total_score >= 50:
        decision = "MAYBE"
        notes = "Conditions are marginal. Proceed with caution and be prepared for changes."
    else: # score < 50
        decision = "NO-GO"
        notes = "Conditions are unfavorable. It is not recommended to proceed."

    # Handle insufficient data case
    if len(scores) == 1 and not hard_stop_reasons:
        decision = "INSUFFICIENT DATA"
        notes = "Only one weather metric was available. The assessment may not be reliable."

    return HeuristicOutput(
        decision=decision,
        notes=notes,
        weighted_score=total_score,
        reasons=[], # 'reasons' field is kept for future use, not populated by this engine
        hard_stop_reasons=hard_stop_reasons
    )
