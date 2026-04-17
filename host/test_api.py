import requests
import time
from datetime import datetime, timezone
from config import API_KEY, BASE_URL, GREEN_LINE_STOP, BUS_39_STOP, REFRESH_RATE

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
            if diff >= 2:
                minutes.append(int(diff))
            if len(minutes) == 3:
                break

        return minutes

    except Exception as e:
        print(f"API error: {e}")
        return []

while True:
    green = get_predictions(GREEN_LINE_STOP, "Green-E")
    bus = get_predictions(BUS_39_STOP, "39")

    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}]")
    print(f"Prudential - GL-E - Heath Street:       {green[0]}min" if green else "Prudential - GL-E - Heath Street:       No predictions")
    print(f"Huntington @ Prudential - 39 - Forest Hills: {bus[0]}min" if bus else "Huntington @ Prudential - 39 - Forest Hills: No predictions")

    time.sleep(REFRESH_RATE)