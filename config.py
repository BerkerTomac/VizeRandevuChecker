import os
from dotenv import load_dotenv

load_dotenv()

# API URL
API_URL = "https://api.schengenvisaappointments.com/api/visa-list/?format=json"

# WhatsApp configuration
PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # Format: +905xxxxxxxxx

# Checking interval (in seconds)
CHECK_INTERVAL = 30  # 1 dakka

# Filter settings
SOURCE_COUNTRY = "Turkiye"
MISSION_COUNTRY = "France"