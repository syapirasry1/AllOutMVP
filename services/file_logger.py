import json
from pathlib import Path
from services.models import AssessmentReport
from utils.app_error import AppErrorWrapper

# Define the data directory and the single log file
DATA_DIR = Path(__file__).parent.parent / "data"
LOG_FILE = DATA_DIR / "assessment_log.json"

def log_report_to_file(report: AssessmentReport):
    """
    Appends a given AssessmentReport to a single JSON log file.

    If the file doesn't exist, it's created. The file will contain a list of reports.
    """
    try:
        # Ensure the data directory exists
        DATA_DIR.mkdir(exist_ok=True)
        
        # Read existing reports from the log file
        reports_list = []
        if LOG_FILE.exists():
            with LOG_FILE.open('r', encoding='utf-8') as f:
                try:
                    reports_list = json.load(f)
                    # Ensure it's a list, in case the file is corrupted
                    if not isinstance(reports_list, list):
                        reports_list = []
                except json.JSONDecodeError:
                    # File is empty or corrupted, start a new list
                    reports_list = []
        
        # Append the new report (as a dictionary) to the list
        reports_list.append(report.model_dump())
        
        # Write the updated list back to the file
        with LOG_FILE.open('w', encoding='utf-8') as f:
            json.dump(reports_list, f, indent=4)

    except (IOError, json.JSONDecodeError) as e:
        raise AppErrorWrapper(
            error_code="FILE_LOGGING_IO_ERROR",
            user_message=f"Could not write report to log file: {e}"
        )
    except Exception as e:
        raise AppErrorWrapper(
            error_code="FILE_LOGGING_UNEXPECTED_ERROR",
            user_message=f"An unexpected error occurred while logging the report: {e}"
        )