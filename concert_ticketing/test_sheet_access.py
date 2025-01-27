
# test_sheet_access.py
import gspread
from google.oauth2.service_account import Credentials  # <-- CHANGE THIS

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1w4FrT6AHAVaJIuUi4Rc9MhdwsOCVrexXKUeKzwkgc7A/edit#gid=0"
CREDENTIALS_FILE = "/Users/timchan/concert_ticketing/credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(
            self.creds_path,
            scopes=self.scopes
        )

sheet = client.open_by_url(SPREADSHEET_URL).sheet1
print(sheet.get_all_records())