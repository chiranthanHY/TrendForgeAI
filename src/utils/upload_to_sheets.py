# upload_to_sheets.py (DEBUGGING VERSION)
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from datetime import datetime, timedelta
import os

def upload_to_google_sheet(dataframe, sheet_id_or_name, worksheet_name):
    """
    Uploads a pandas DataFrame to a specified Google Sheet worksheet.
    Assumes you have set up gspread authentication using a service account JSON file.
    
    Args:
        sheet_id_or_name: Either the spreadsheet ID (from URL) or the spreadsheet name/title
        worksheet_name: Name of the worksheet/tab within the spreadsheet
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Look for service_account.json in project root (../../ from src/utils)
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        service_account_path = os.path.join(project_root, "service_account.json")
        
        if not os.path.exists(service_account_path):
             # Try data directory
             service_account_path = os.path.join(project_root, "data", "service_account.json")

        if not os.path.exists(service_account_path):
             # Fallback to CWD if running from root
             service_account_path = os.path.join(os.getcwd(), "service_account.json")

        print(f"DEBUG: Attempting to load service account from: {service_account_path}")
        gc = gspread.service_account(filename=service_account_path) 
        print(f"DEBUG: Service account loaded successfully.")

        print(f"DEBUG: Attempting to open spreadsheet: '{sheet_id_or_name}'")
        try:
            # Try to open by ID first (more reliable)
            if len(sheet_id_or_name) > 30:  # Likely a spreadsheet ID
                spreadsheet = gc.open_by_key(sheet_id_or_name)
                print(f"DEBUG: Spreadsheet opened by ID successfully.")
            else:  # Likely a spreadsheet name
                spreadsheet = gc.open(sheet_id_or_name)
                print(f"DEBUG: Spreadsheet '{sheet_id_or_name}' opened by name successfully.")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"ERROR: Spreadsheet '{sheet_id_or_name}' not found. Please ensure the spreadsheet exists and is shared with your service account.")
            return # Exit function if primary spreadsheet not found
        
        # Get or create the worksheet
        print(f"DEBUG: Attempting to find or create worksheet: '{worksheet_name}'")
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            print(f"DEBUG: Found existing worksheet: '{worksheet_name}'")
        except gspread.exceptions.WorksheetNotFound:
            print(f"DEBUG: Worksheet '{worksheet_name}' not found, attempting to create it...")
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="50")
            print(f"DEBUG: Created new worksheet: '{worksheet_name}' successfully.")

        print(f"DEBUG: Clearing existing data in worksheet '{worksheet_name}'...")
        worksheet.clear()
        print(f"DEBUG: Data cleared.")

        print(f"DEBUG: Uploading DataFrame to worksheet '{worksheet_name}'...")
        set_with_dataframe(worksheet, dataframe)
        print(f"DEBUG: Successfully uploaded data to Google Sheet, worksheet '{worksheet_name}'")

    except gspread.exceptions.APIError as e:
        print(f"\nCRITICAL GOOGLE SHEETS API ERROR: {e}")
        print("Please ensure:")
        print("  1. Your service account JSON file is valid and for the correct project.")
        print(f"  2. The Google Sheet is explicitly shared with the service account's email address.")
        print("  3. The 'Google Drive API' and 'Google Sheets API' are enabled in your Google Cloud Project.")
        print("  4. The service account has 'Editor' role on the Google Cloud Project and/or the specific Google Sheet.")
    except FileNotFoundError:
        print(f"\nERROR: 'service_account.json' file not found at the expected path: {service_account_path}")
        print("Please ensure your Google Sheets service account JSON key file is correctly named and located.")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR during Google Sheets upload: {type(e).__name__}: {e}")
        print("This error is general. Please review previous DEBUG messages for clues.")
    
# Example of how you might test this function independently (optional)
if __name__ == '__main__':
    print("Running a test upload to Google Sheets...")
    test_data = {
        'col1': [1, 2, 3],
        'col2': ['A', 'B', 'C'],
        'date': [datetime.now(), datetime.now() - timedelta(days=1), datetime.now() - timedelta(days=2)]
    }
    test_df = pd.DataFrame(test_data)
    
    # Use your actual spreadsheet ID here
    upload_to_google_sheet(test_df, "1gNHWjMghm4kTVbFSgC298LgWOWhgREY2wRRzTq-yHrk", "Test_Upload")
    print("Test upload script finished.")