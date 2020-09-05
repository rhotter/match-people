from dotenv import load_dotenv
import os

load_dotenv()

spreadsheet_id = os.getenv("SPREADSHEET_ID")
spreadsheet_range = os.getenv("SPREADSHEET_RANGE")

personality_spreadsheet_id = os.getenv("PERSONALITY_TEST_SPREADSHEET_ID")
personality_spreadsheet_range = os.getenv("PERSONALITY_TEST_SPREADSHEET_RANGE")