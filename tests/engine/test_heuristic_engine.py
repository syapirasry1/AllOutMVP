# tests/engine/test_heuristic_engine.py
import pytest
from engine.heuristic_engine import run_heuristic_engine
from engine.models import HeuristicInput

def create_input(**kwargs):
    """Creates a HeuristicInput with default safe values."""
    defaults = {
        "temp_c": 20.0,
        "feelslike_c": 20.0,
        "wind_mph": 10.0,
        "precip_mm": 0.0,
        "uv_index": 5.0,
        "daily_chance_of_rain": 20,
        "heat_index_c": 20.0,
        "wind_chill_c": 20.0,
        "pop_percent": 20,
        "precip_rate_mmhr": 0.0,
    }
    defaults.update(kwargs)
    return HeuristicInput(**defaults)

# --- Test Cases for Final Decisions ---

def test_perfect_conditions_go():
    """Test for a clear GO decision with perfect weather."""
    perfect_input = create_input(
        wind_mph=5,
        heat_index_c=20,
        pop_percent=10,
        precip_rate_mmhr=0,
        uv_index=1
    )
    result = run_heuristic_engine(perfect_input)
    assert result.decision == "GO"
    assert result.weighted_score == 100.0
    assert not result.hard_stop_reasons

def test_marginal_conditions_maybe():
    """Test for a MAYBE decision with marginal weather."""
    marginal_input = create_input(
        wind_mph=25,       # Amber (50 * 0.20 = 10)
        heat_index_c=28,   # Amber (50 * 0.35 = 17.5)
        pop_percent=50,    # Amber (50 * 0.40 = 20)
        precip_rate_mmhr=1.0,
        uv_index=5         # Amber (50 * 0.05 = 2.5)
    )
    result = run_heuristic_engine(marginal_input)
    assert result.decision == "MAYBE"
    assert result.weighted_score == pytest.approx(50.0)
    assert not result.hard_stop_reasons

def test_poor_conditions_no_go():
    """Test for a NO-GO decision from low score."""
    poor_input = create_input(
        wind_mph=25,       # Amber (50 * 0.20 = 10)
        heat_index_c=10,   # Green (100 * 0.35 = 35)
        pop_percent=90,    # Red (0 * 0.40 = 0)
        precip_rate_mmhr=5.0,
        uv_index=9         # Red (0 * 0.05 = 0)
    )
    result = run_heuristic_engine(poor_input)
    assert result.decision == "NO-GO"
    assert result.weighted_score == pytest.approx(45.0)
    assert "Heavy precipitation rate (> 4.0 mm/hr)." in result.hard_stop_reasons

# --- Test Cases for Hard-Stops ---

@pytest.mark.parametrize("wind_speed, reason", [
    (32, "Wind speed is at a dangerous level (>= 32 mph)."),
    (40, "Wind speed is at a dangerous level (>= 32 mph).")
])
def test_wind_hard_stop(wind_speed, reason):
    """Test that high wind speed triggers a hard-stop NO-GO."""
    test_input = create_input(wind_mph=wind_speed, heat_index_c=20)
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO-GO"
    assert reason in result.hard_stop_reasons

@pytest.mark.parametrize("temp, reason", [
    (41, "Extreme heat warning (feels like >= 41°C)."),
    (-28, "Extreme cold warning (feels like <= -28°C).")
])
def test_thermal_hard_stop(temp, reason):
    """Test that extreme temperatures trigger a hard-stop NO-GO."""
    test_input = create_input(heat_index_c=temp, wind_mph=5)
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO-GO"
    assert reason in result.hard_stop_reasons

def test_precip_hard_stop():
    """Test that heavy precipitation triggers a hard-stop NO-GO."""
    test_input = create_input(pop_percent=80, precip_rate_mmhr=4.1, wind_mph=5)
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO-GO"
    assert "Heavy precipitation rate (> 4.0 mm/hr)." in result.hard_stop_reasons

def test_multiple_hard_stops():
    """Test that multiple hard-stops are all listed."""
    test_input = create_input(wind_mph=35, heat_index_c=42)
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO-GO"
    assert len(result.hard_stop_reasons) == 2
    assert "Wind speed is at a dangerous level (>= 32 mph)." in result.hard_stop_reasons
    assert "Extreme heat warning (feels like >= 41°C)." in result.hard_stop_reasons

# --- Test Cases for Edge Cases (Data Availability) ---

def test_no_data():
    """Test for NO DATA decision when no metrics are available."""
    # FIX: Pass None for all optional metrics
    test_input = create_input(
        wind_mph=None,
        heat_index_c=None,
        uv_index=None,
        pop_percent=None,
        precip_rate_mmhr=None
    )
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO DATA"


def test_insufficient_data():
    """Test for INSUFFICIENT DATA when only one metric is available."""
    # FIX: Only provide wind_mph, set others to None
    test_input = create_input(
        wind_mph=10.0,
        heat_index_c=None,
        uv_index=None,
        pop_percent=None,
        precip_rate_mmhr=None
    )
    result = run_heuristic_engine(test_input)
    assert result.decision == "INSUFFICIENT DATA"


def test_partial_data_score_calculation():
    """Test that score is calculated correctly with missing metrics (no renormalization)."""
    # Missing UV and Precip
    test_input = create_input(
        wind_mph=10.0,
        heat_index_c=30.0,
        uv_index=None,  # FIX: None means missing
        pop_percent=None,  # FIX: None means missing
        precip_rate_mmhr=None  # FIX: None means missing
    )
    # Expected score = (100 * 0.20) + (50 * 0.35) = 20 + 17.5 = 37.5
    result = run_heuristic_engine(test_input)
    assert result.decision == "NO-GO"  # Score < 50
    assert 37.0 <= result.weighted_score <= 38.0  # Allow small tolerance