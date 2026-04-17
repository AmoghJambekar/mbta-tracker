import os
from dotenv import load_dotenv

load_dotenv()

# MBTA API
API_KEY = os.getenv("MBTA_API_KEY")
BASE_URL = "https://api-v3.mbta.com"

# Stop IDs
GREEN_LINE_STOP = "70241"   # Green Line E, Prudential outbound
BUS_39_STOP = "2716"        # Route 39, Huntington Ave @ Prudential outbound

# How often to poll the API (seconds)
REFRESH_RATE = 30

# Serial port - set this in your .env to match your machine
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/tty.usbmodem1101")
BAUD_RATE = 9600