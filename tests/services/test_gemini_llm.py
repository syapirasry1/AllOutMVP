import pytest
from unittest.mock import patch, MagicMock
import google.api_core.exceptions

from services.gemini_llm import GeminiLLMClient
from services.models import GeminiInput, CurrentWeatherForGemini, DayForecastForGemini, GeminiOutput
from engine.models import HeuristicOutput
from utils.app_error import AppErrorWrapper


@pytest.fixture
def mock_genai():
    """Mock the google.generativeai module."""
    with patch('services.gemini_llm.genai') as mock:
        yield mock


@pytest.fixture
def gemini_client(monkeypatch):
    """Create a GeminiLLMClient with a mocked API key."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key-12345")
    return GeminiLLMClient()


@pytest.fixture
def sample_gemini_input():
    """Create a sample GeminiInput for testing."""
    return GeminiInput(
        location_name="Test City",
        current_weather=CurrentWeatherForGemini(
            temp_c=20.0,
            feelslike_c=18.0,
            wind_mph=10.0,
            precip_mm=0.0,
            uv=5.0
        ),
        day_forecast=DayForecastForGemini(
            daily_chance_of_rain=20
        ),
        heuristic_output=HeuristicOutput(
            decision="GO",
            weighted_score=85.0,
            notes="Conditions are good.",
            reasons=["Good weather"]
        )
    )


def test_initialization_success(monkeypatch):
    """Test successful initialization with API key."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    client = GeminiLLMClient()
    assert client.model is not None


def test_initialization_missing_api_key(monkeypatch):
    """Test that missing API key raises AppErrorWrapper."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        GeminiLLMClient()
    
    assert exc_info.value.error_code == "GEMINI_API_KEY_MISSING"


def test_get_explanation_success(mock_genai, gemini_client, sample_gemini_input):
    """Test successful explanation generation."""
    mock_response = MagicMock()
    mock_response.prompt_feedback.block_reason = None
    mock_response.candidates = [MagicMock()]
    mock_response.candidates[0].finish_reason.name = 'STOP'
    mock_response.candidates[0].content.parts = [MagicMock()]
    mock_response.candidates[0].content.parts[0].text = "This is a test explanation."
    
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    result = gemini_client.get_explanation(sample_gemini_input)
    
    assert isinstance(result, GeminiOutput)
    assert result.explanation == "This is a test explanation."


def test_get_explanation_validation_error(mock_genai, gemini_client, sample_gemini_input):
    """Test that exceeding word count raises AppErrorWrapper."""
    # Create a response that exceeds 350 words
    long_text = " ".join(["word"] * 351)
    
    mock_response = MagicMock()
    mock_response.prompt_feedback.block_reason = None
    mock_response.candidates = [MagicMock()]
    mock_response.candidates[0].finish_reason.name = 'STOP'
    mock_response.candidates[0].content.parts = [MagicMock()]
    mock_response.candidates[0].content.parts[0].text = long_text
    
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_VALIDATION_ERROR"
    assert "350" in exc_info.value.user_message


def test_prompt_blocked(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of prompt blocked by safety filters."""
    mock_response = MagicMock()
    mock_response.prompt_feedback.block_reason = MagicMock()
    mock_response.prompt_feedback.block_reason.name = "SAFETY"
    
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_PROMPT_BLOCKED"


def test_response_blocked(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of response blocked by safety filters."""
    mock_response = MagicMock()
    mock_response.prompt_feedback.block_reason = None
    mock_response.candidates = [MagicMock()]
    mock_response.candidates[0].finish_reason.name = 'SAFETY'
    
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_RESPONSE_BLOCKED"


def test_empty_response(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of empty response."""
    mock_response = MagicMock()
    mock_response.prompt_feedback.block_reason = None
    mock_response.candidates = []
    
    mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_EMPTY_RESPONSE"


def test_api_error(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of general API errors."""
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = \
        google.api_core.exceptions.GoogleAPICallError("API Error")
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_API_ERROR"


def test_timeout_error(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of timeout errors."""
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = \
        google.api_core.exceptions.DeadlineExceeded("Timeout")
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_TIMEOUT"


def test_unexpected_error(mock_genai, gemini_client, sample_gemini_input):
    """Test handling of unexpected errors."""
    mock_genai.GenerativeModel.return_value.generate_content.side_effect = \
        Exception("Unexpected error")
    
    with pytest.raises(AppErrorWrapper) as exc_info:
        gemini_client.get_explanation(sample_gemini_input)
    
    assert exc_info.value.error_code == "GEMINI_UNEXPECTED_ERROR"
