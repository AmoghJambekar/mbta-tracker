import requests
import time
from datetime import datetime, timezone
from colorama import init, Fore, Style
from config import API_KEY, BASE_URL, GREEN_LINE_STOP, BUS_39_STOP, REFRESH_RATE

init(autoreset=True)

DIVIDER = " " + "─" * 26

def get_predictions(stop_id, route_id):
    url = f"{BASE_URL}/predictions"
    params = {
        "filter[stop]": stop_id,
        "filter[route]": route_id,
        "sort": "departure_time",
        "api_key": API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]

        minutes = []
        now = datetime.now(timezone.utc)

        for prediction in data:
            departure = prediction["attributes"].get("departure_time")
            if not departure:
                continue
            departure_dt = datetime.fromisoformat(departure)
            diff = (departure_dt - now).total_seconds() / 60
            if diff >= 0:
                minutes.append(int(diff))
            if len(minutes) == 3:
                break

        return minutes

    except Exception as e:
        print(f"API error: {e}")
        return []

def format_time(minutes):
    if not minutes:
        return "No service"
    if minutes[0] == 0:
        return "ARR"
    return f"{minutes[0]}min"

while True:
    green = get_predictions(GREEN_LINE_STOP, "Green-E")
    bus = get_predictions(BUS_39_STOP, "39")

    now = datetime.now().strftime("%H:%M:%S")

    print(DIVIDER)
    print(DIVIDER)
    print(f" {Fore.GREEN}GL-E{Style.RESET_ALL}  > Heath St      {format_time(green)}")
    print(f" {Fore.YELLOW}39{Style.RESET_ALL}    > Forest Hills  {format_time(bus)}")
    print(DIVIDER)
    print(f" Last updated: {now}")

    time.sleep(REFRESH_RATE)