import os
from dotenv import load_dotenv

load_dotenv()

# MBTA API
API_KEY = os.getenv("MBTA_API_KEY")
BASE_URL = "https://api-v3.mbta.com"

# Stop IDs
GREEN_LINE_STOP = "70241"   # Green Line E, Prudential outbound
BUS_39_STOP = "11389"   # Route 39, Huntington Ave @ Prudential Station       # Route 39, Huntington Ave @ Prudential outbound

REFRESH_RATE = 30

# Serial port
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/tty.usbmodem1101")
BAUD_RATE = 9600