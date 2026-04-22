"""Shared MBTA API v3 client for predictions."""

import requests
from datetime import datetime, timezone

from config import API_KEY, BASE_URL


def get_predictions(stop_id, route_id, max_predictions=3):
    """Fetch upcoming departure times in minutes for a stop and route."""
    url = f"{BASE_URL}/predictions"
    params = {
        "filter[stop]": stop_id,
        "filter[route]": route_id,
        "sort": "departure_time",
        "api_key": API_KEY,
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
            if len(minutes) == max_predictions:
                break

        return minutes

    except Exception as e:
        print(f"API error for stop {stop_id}: {e}")
        return []
