import streamlit as st
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- Real Clients ---
from services.weather_api import WeatherApiClient
from services.gemini_llm import GeminiLLMClient

from services.report_generator import generate_report
from services.file_logger import log_report_to_file
from utils.app_error import AppErrorWrapper
from utils.validation import sanitize_location_input
from engine.heuristic_engine import run_heuristic_engine
from engine.models import HeuristicInput
from services.models import GeminiInput, CurrentWeatherForGemini, DayForecastForGemini, AssessmentReport

# --- Page Configuration ---
st.set_page_config(
    page_title="AllOut Weather Buddy",
    page_icon="🏔️",
    layout="wide"
)

# --- Helper Function for TXT Export (Story 5.2) ---
def _format_report_as_text(report: AssessmentReport) -> str:
    """
    Formats an AssessmentReport as a human-readable text string.
    
    Args:
        report: The AssessmentReport to format
        
    Returns:
        A formatted string suitable for TXT export
    """
    lines = []
    lines.append("=" * 70)
    lines.append("ALLOUT - OUTDOOR SAFETY ASSESSMENT REPORT")
    lines.append("=" * 70)
    lines.append("")
    
    # Header Information
    lines.append(f"Location: {report.location_name}")
    lines.append(f"Assessment Date: {report.assessment_date}")
    lines.append(f"Generated: {report.assessment_timestamp_utc}")
    lines.append(f"Report ID: {report.report_id}")
    lines.append("")
    
    # Weather Conditions
    lines.append("-" * 70)
    lines.append("CURRENT WEATHER CONDITIONS")
    lines.append("-" * 70)
    current = report.weather_data.current
    lines.append(f"Temperature: {current.temp_c}°C (Feels like: {current.feelslike_c}°C)")
    lines.append(f"Wind Speed: {current.wind_mph} mph")
    lines.append(f"Precipitation: {current.precip_mm} mm")
    lines.append(f"UV Index: {current.uv}")
    lines.append("")
    
    # Forecast
    forecast_day = report.weather_data.forecast.forecastday[0]
    lines.append(f"Daily Chance of Rain: {forecast_day.day.daily_chance_of_rain}%")
    lines.append(f"Temperature Range: {forecast_day.day.mintemp_c}°C - {forecast_day.day.maxtemp_c}°C")
    lines.append("")
    
    # Heuristic Decision
    lines.append("-" * 70)
    lines.append("HEURISTIC ANALYSIS")
    lines.append("-" * 70)
    heuristic = report.heuristic_output
    lines.append(f"Decision: {heuristic.decision}")
    
    if heuristic.weighted_score is not None:
        lines.append(f"Safety Score: {heuristic.weighted_score:.1f}/100")
    
    if heuristic.hard_stop_reasons:
        lines.append("\nHard Stop Warnings:")
        for reason in heuristic.hard_stop_reasons:
            lines.append(f"  ⚠️  {reason}")
    
    if heuristic.reasons:
        lines.append("\nReasoning:")
        for reason in heuristic.reasons:
            lines.append(f"  • {reason}")
    
    if heuristic.notes:
        lines.append(f"\nNotes: {heuristic.notes}")
    
    lines.append("")
    
    # AI Explanation
    lines.append("-" * 70)
    lines.append("AI ANALYSIS")
    lines.append("-" * 70)
    lines.append(report.ai_explanation.explanation)
    lines.append("")
    
    lines.append("=" * 70)
    lines.append("End of Report")
    lines.append("=" * 70)
    
    return "\n".join(lines)

# --- UI Components ---
st.title("AllOut Safety Assessment")
st.write("Your outdoor safety buddy. Get a clear Go/No-Go decision for your planned activity.")

# --- Inputs ---
location_input = st.text_input("Enter Location", "Coventry", key="location")
assessment_date = st.date_input("Select Assessment Date", datetime.date.today())

# --- Trigger ---
if st.button("Assess Safety", type="primary"):
    try:
        sanitized_location = sanitize_location_input(location_input)
        if not sanitized_location:
            st.error("Please enter a valid location.")
        else:
            with st.spinner("Assessing conditions..."):
                
                # Always use real clients
                weather_client = WeatherApiClient()
                gemini_client = GeminiLLMClient()

                # 1. Get Weather Data
                weather_data = weather_client.get_weather_data(
                    location=sanitized_location,
                    date=assessment_date.strftime("%Y-%m-%d")
                )

                # 2. Run Heuristic Engine
                heuristic_input = HeuristicInput(
                    temp_c=weather_data.current.temp_c,
                    feelslike_c=weather_data.current.feelslike_c,
                    wind_mph=weather_data.current.wind_mph,
                    precip_mm=weather_data.current.precip_mm,
                    uv_index=weather_data.current.uv,
                    daily_chance_of_rain=weather_data.forecast.forecastday[0].day.daily_chance_of_rain,
                    heat_index_c=weather_data.current.feelslike_c,
                    wind_chill_c=weather_data.current.feelslike_c,
                    pop_percent=weather_data.forecast.forecastday[0].day.daily_chance_of_rain,
                    precip_rate_mmhr=weather_data.current.precip_mm
                )
                heuristic_result = run_heuristic_engine(heuristic_input)

                # 3. Get AI Explanation
                gemini_input = GeminiInput(
                    location_name=weather_data.location.name,
                    current_weather=CurrentWeatherForGemini(
                        temp_c=weather_data.current.temp_c,
                        feelslike_c=weather_data.current.feelslike_c,
                        wind_mph=weather_data.current.wind_mph,
                        precip_mm=weather_data.current.precip_mm,
                        uv=weather_data.current.uv
                    ),
                    day_forecast=DayForecastForGemini(
                        daily_chance_of_rain=weather_data.forecast.forecastday[0].day.daily_chance_of_rain,
                        uv=weather_data.current.uv
                    ),
                    heuristic_output=heuristic_result
                )
                
                # NEW: Graceful Fallback for 429 Rate Limit Errors
                try:
                    gemini_output = gemini_client.get_explanation(gemini_input)
                except AppErrorWrapper as e:
                    if e.error_code == "GEMINI_API_ERROR" and "429" in e.user_message:
                        # Show friendly warning with error details
                        st.warning("⚠️ **AI Service Temporarily Unavailable**")
                        st.caption(f"🔍 Error Code: 429 - Rate Limit Exceeded | Error Type: {e.error_code}")
                        st.info("💡 Showing general safety guidance based on conditions assessment...")
                        
                        # Context-aware fallback based on heuristic decision
                        decision = heuristic_result.decision
                        
                        if decision == "GO":
                            fallback_message = (
                                "**Conditions appear favorable for outdoor activities.** "
                                "The current weather metrics suggest safe conditions. However, always:\n\n"
                                "✅ Check the latest weather updates before departing\n\n"
                                "✅ Inform someone of your plans and expected return time\n\n"
                                "✅ Pack essential safety gear (first aid, navigation, communication)\n\n"
                                "✅ Bring layers and rain protection - weather can change quickly\n\n"
                                "✅ Monitor conditions throughout your activity\n\n"
                                "Stay alert to any weather changes and trust your judgment. "
                                "If conditions deteriorate, don't hesitate to turn back."
                            )
                        elif decision == "MAYBE":
                            fallback_message = (
                                "**Conditions are borderline - proceed with caution.** "
                                "Our analysis indicates marginal weather conditions. Consider these recommendations:\n\n"
                                "⚠️ Re-check weather forecasts from multiple sources\n\n"
                                "⚠️ Have a backup plan and clear turnaround criteria\n\n"
                                "⚠️ Ensure all participants are experienced and properly equipped\n\n"
                                "⚠️ Start early to allow time for changing conditions\n\n"
                                "⚠️ Be prepared to cancel or turn back if conditions worsen\n\n"
                                "Borderline conditions require extra vigilance. It's always better to postpone "
                                "than to take unnecessary risks. Your safety is the priority."
                            )
                        else:  # NO-GO
                            fallback_message = (
                                "**Conditions are not favorable - outdoor activities not recommended.** "
                                "Our safety analysis indicates significant risks. Here's why this matters:\n\n"
                                "❌ Current weather metrics exceed safe thresholds\n\n"
                                "❌ High risk of dangerous conditions during your planned activity\n\n"
                                "❌ Increased chance of weather-related incidents\n\n"
                                "**Recommended Actions:**\n\n"
                                "• Postpone your outdoor plans to a safer day\n\n"
                                "• Consider alternative indoor activities\n\n"
                                "• If you must go out, take extreme precautions and stay in sheltered areas\n\n"
                                "• Monitor weather updates for improvement\n\n"
                                "Remember: Mountains, trails, and outdoor activities will always be there. "
                                "Your safety cannot be compromised."
                            )
                        
                        # Create fallback GeminiOutput
                        from services.models import GeminiOutput
                        gemini_output = GeminiOutput(explanation=fallback_message)
                    else:
                        # For other non-429 Gemini errors, re-raise
                        raise e

                # 4. Generate and Log Report
                assessment_report = generate_report(
                    location_name=weather_data.location.name,
                    assessment_date=assessment_date.strftime("%Y-%m-%d"),
                    weather_data=weather_data,
                    heuristic_output=heuristic_result,
                    ai_explanation=gemini_output,
                )
                
                # Always log
                log_report_to_file(assessment_report)

            # --- Results Display ---
            st.subheader(f"Safety Assessment for {weather_data.location.name} on {assessment_date.strftime('%Y-%m-%d')}")

            # === STORY 1.4: Enhanced Visual Safety Indicator ===
            # Create large, color-coded decision indicator with emojis
            
            if heuristic_result.decision == "GO":
                st.success(f"# ✅ GO\n\n### {heuristic_result.notes}")
                
            elif heuristic_result.decision == "MAYBE":
                st.warning(f"# ⚠️ MAYBE\n\n### {heuristic_result.notes}")
                
            elif heuristic_result.decision == "NO-GO":
                st.error(f"# 🛑 NO-GO\n\n### {heuristic_result.notes}")
                
            elif heuristic_result.decision in ["INSUFFICIENT DATA", "NO DATA"]:
                st.info(f"# ℹ️ {heuristic_result.decision}\n\n### {heuristic_result.notes}")

            st.info(f"**AI Safety Advice:** {gemini_output.explanation}")

            # Score and Hard-Stops
            col1, col2 = st.columns([1, 2])
            with col1:
                if heuristic_result.weighted_score is not None:
                    st.metric("Safety Score", value=f"{heuristic_result.weighted_score:.0f}/100")
            
            with col2:
                if heuristic_result.hard_stop_reasons:
                    st.write("**Hard-Stop Reasons:**")
                    for reason in heuristic_result.hard_stop_reasons:
                        st.markdown(f"- {reason}")
            
            st.divider()

            # Weather Grid
            st.subheader("Key Weather Metrics")
            cols = st.columns(5)  # Changed from 4 to 5
            with cols[0]:
                st.metric("Wind Speed", f"{weather_data.current.wind_mph} mph")
            with cols[1]:
                st.metric("Feels Like", f"{weather_data.current.feelslike_c}°C")
            with cols[2]:
                st.metric("UV Index", f"{weather_data.current.uv}")
            with cols[3]:
                st.metric("Rain Chance", f"{weather_data.forecast.forecastday[0].day.daily_chance_of_rain}%")
            with cols[4]:
                st.metric("Precipitation", f"{weather_data.current.precip_mm} mm")

            # === STORY 5.2: Export Report Buttons ===
            st.divider()
            st.subheader("📥 Export Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # JSON Export
                json_data = assessment_report.model_dump_json(indent=2)
                json_filename = f"AllOut_{weather_data.location.name.replace(' ', '_')}_{assessment_date.strftime('%Y-%m-%d')}.json"
                
                st.download_button(
                    label="📄 Download JSON",
                    data=json_data,
                    file_name=json_filename,
                    mime="application/json",
                    help="Download the complete report as a JSON file for data processing or archiving",
                    use_container_width=True
                )
            
            with col2:
                # TXT Export
                txt_data = _format_report_as_text(assessment_report)
                txt_filename = f"AllOut_{weather_data.location.name.replace(' ', '_')}_{assessment_date.strftime('%Y-%m-%d')}.txt"
                
                st.download_button(
                    label="📝 Download TXT",
                    data=txt_data,
                    file_name=txt_filename,
                    mime="text/plain",
                    help="Download a human-readable summary as a text file for easy reading",
                    use_container_width=True
                )

    # FIX: Only catch NON-Gemini errors here (Weather API errors, validation errors, etc.)
    except AppErrorWrapper as e:
        # Only show error UI if it's NOT a Gemini 429 (those are handled gracefully above)
        if not (e.error_code == "GEMINI_API_ERROR" and "429" in str(e)):
            st.error(f"**{e.error_code}:** {e.user_message}")
    except Exception as e:
        print(f"--- DEBUG: An unexpected exception occurred in app.py: {e} ---")
        st.error(f"An unexpected error occurred: {e}")

