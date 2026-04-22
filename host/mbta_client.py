"""Shared MBTA API v3 client for predictions."""

import requests
from datetime import datetime, timezone

from config import API_KEY, BASE_URL


def _parse_departure(departure: str) -> datetime:
    """Parse MBTA RFC3339 times; map trailing Z for Python < 3.11 fromisoformat."""
    if departure.endswith("Z"):
        departure = departure[:-1] + "+00:00"
    dt = datetime.fromisoformat(departure)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def get_predictions(stop_id, route_id, max_predictions=3):
    """Fetch upcoming departure times in minutes for a stop and route."""
    if not API_KEY:
        print("MBTA_API_KEY is not set; copy .env.example to host/.env and add your key.")
        return []

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
            departure_dt = _parse_departure(departure)
            diff = (departure_dt - now).total_seconds() / 60
            if diff >= 0:
                minutes.append(int(diff))
            if len(minutes) == max_predictions:
                break

        return minutes

    except Exception as e:
        print(f"API error for stop {stop_id}: {e}")
        return []
