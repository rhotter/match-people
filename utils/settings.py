from dotenv import load_dotenv
import os

load_dotenv()

spreadsheet_id = os.getenv("SPREADSHEET_ID")
spreadsheet_range = os.getenv("SPREADSHEET_RANGE")