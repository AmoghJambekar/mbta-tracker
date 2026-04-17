import requests
import serial
import time
from datetime import datetime, timezone
from config import API_KEY, BASE_URL, GREEN_LINE_STOP, BUS_39_STOP, REFRESH_RATE, SERIAL_PORT, BAUD_RATE

def get_predictions(stop_id, route_id):
    """Fetch next departure predictions from MBTA API for a given stop and route."""
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
        print(f"API error for stop {stop_id}: {e}")
        return []

def format_line(label, minutes):
    """Format a 16 character wide LCD line from a label and list of minutes."""
    if not minutes:
        times = "--  --  --"
    else:
        # Pad to always show 3 slots
        slots = (minutes + ["--", "--"])[:3]
        times = "  ".join(f"{m}m" if isinstance(m, int) else m for m in slots)

    line = f"{label}{times}"
    # Truncate or pad to exactly 16 chars
    return line[:16].ljust(16)

def build_message(green_mins, bus_mins):
    """Build the full 2-line message to send to the Pico."""
    line1 = format_line("E:  ", green_mins)
    line2 = format_line("39: ", bus_mins)
    # Pipe separates the two lines, newline signals end of message
    return f"{line1}|{line2}\n"

def send_to_pico(ser, message):
    """Send formatted message over serial to the Pico."""
    try:
        ser.write(message.encode("utf-8"))
        print(f"Sent to Pico: {message.strip()}")
    except Exception as e:
        print(f"Serial error: {e}")

def main():
    print(f"Connecting to Pico on {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Give serial connection time to settle
        print("Connected!")
    except Exception as e:
        print(f"Could not open serial port: {e}")
        return

    print("Starting MBTA tracker — polling every {REFRESH_RATE}s")

    while True:
        print("\nFetching predictions...")

        green_mins = get_predictions(GREEN_LINE_STOP, "Green-E")
        bus_mins = get_predictions(BUS_39_STOP, "39")

        print(f"Green Line E: {green_mins}")
        print(f"Route 39:     {bus_mins}")

        message = build_message(green_mins, bus_mins)
        send_to_pico(ser, message)

        time.sleep(REFRESH_RATE)

if __name__ == "__main__":
    main()