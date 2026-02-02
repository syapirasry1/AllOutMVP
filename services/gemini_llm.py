import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.api_core.exceptions
from pydantic import ValidationError
import streamlit as st

from utils.app_error import AppErrorWrapper
from services.models import GeminiInput, GeminiOutput

# Load environment variables once at module level
load_dotenv()


class GeminiLLMClient:
    def __init__(self):
        """Initialize Gemini client with API key and safety settings."""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            api_key = api_key.strip()
        
        if not api_key:
            raise AppErrorWrapper(
                error_code="GEMINI_API_KEY_MISSING",
                user_message="GEMINI_API_KEY not found in environment variables."
            )
        
        genai.configure(api_key=api_key)
        
        # Configure the model with permissive safety thresholds using the correct enum
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            safety_settings=safety_settings
        )

    def get_explanation(self, gemini_input: GeminiInput) -> GeminiOutput:
        """Generate an AI explanation for the assessment."""
        try:
            prompt = self._build_prompt(gemini_input)
            
            # Call Gemini API with proper exception handling
            try:
                response = self.model.generate_content(prompt)
            except google.api_core.exceptions.DeadlineExceeded:
                raise AppErrorWrapper(
                    error_code="GEMINI_TIMEOUT",
                    user_message="Gemini API request timed out. Please try again."
                )
            except google.api_core.exceptions.GoogleAPICallError as e:
                raise AppErrorWrapper(
                    error_code="GEMINI_API_ERROR",
                    user_message=f"Gemini API error: {str(e)}"
                )
            
            # === CHECK 1: Prompt Blocked ===
            if response.prompt_feedback.block_reason:
                raise AppErrorWrapper(
                    error_code="GEMINI_PROMPT_BLOCKED",
                    user_message=f"Your request was blocked by safety filters. Reason: {response.prompt_feedback.block_reason.name}"
                )
            
            # === CHECK 2: Empty Candidates ===
            if not response.candidates:
                raise AppErrorWrapper(
                    error_code="GEMINI_EMPTY_RESPONSE",
                    user_message="No response received from Gemini API."
                )
            
            candidate = response.candidates[0]
            
            # === CHECK 3: Response Blocked ===
            if candidate.finish_reason.name != 'STOP':
                raise AppErrorWrapper(
                    error_code="GEMINI_RESPONSE_BLOCKED",
                    user_message=f"Response was blocked by safety filters. Reason: {candidate.finish_reason.name}"
                )
            
            # === CHECK 4: Extract Text ===
            if not candidate.content.parts:
                raise AppErrorWrapper(
                    error_code="GEMINI_EMPTY_RESPONSE",
                    user_message="No content in response."
                )
            
            explanation_text = candidate.content.parts[0].text
            
            # === CHECK 5: Empty/Whitespace Text ===
            if not explanation_text or not explanation_text.strip():
                raise AppErrorWrapper(
                    error_code="GEMINI_EMPTY_RESPONSE",
                    user_message="Received empty explanation from Gemini."
                )
            
            # === CHECK 6: Validate Output ===
            try:
                output = GeminiOutput(explanation=explanation_text.strip())
                return output
            except ValidationError as e:
                raise AppErrorWrapper(
                    error_code="GEMINI_VALIDATION_ERROR",
                    user_message=f"Generated explanation failed validation: {str(e)}"
                )
        
        except AppErrorWrapper:
            # Re-raise AppErrorWrapper (our custom errors)
            raise
        except Exception as e:
            # Catch any other unexpected errors
            raise AppErrorWrapper(
                error_code="GEMINI_UNEXPECTED_ERROR",
                user_message=f"Unexpected error from Gemini: {str(e)}"
            )

    def _build_prompt(self, gemini_input: GeminiInput) -> str:
        """Build an enhanced prompt with clothing and practical tips."""
        return f"""You are a helpful outdoor activities safety advisor. 
Provide a brief explanation of the weather assessment, followed by 3 specific practical recommendations.

**Weather Conditions:**
- Location: {gemini_input.location_name}
- Temperature: {gemini_input.current_weather.temp_c}°C (feels like {gemini_input.current_weather.feelslike_c}°C)
- Wind: {gemini_input.current_weather.wind_mph} mph
- Precipitation: {gemini_input.current_weather.precip_mm} mm
- UV Index: {gemini_input.current_weather.uv}
- Chance of Rain: {gemini_input.day_forecast.daily_chance_of_rain}%

**Safety Assessment:**
- Decision: {gemini_input.heuristic_output.decision}
- Safety Score: {gemini_input.heuristic_output.weighted_score}/100
- Notes: {gemini_input.heuristic_output.notes}

Provide your response in this EXACT format:

**Weather Summary:** [1-2 sentences explaining the decision based on key weather factors]

**Practical Recommendations:**
1. **Clothing:** [Specific clothing advice for these conditions]
2. **Safety Tip:** [One practical non-clothing safety tip]
3. **Activity Tip:** [One practical non-clothing activity planning tip]

Keep the total response under 200 words. Be specific and actionable.
"""