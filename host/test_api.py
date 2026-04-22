"""Console test harness for MBTA predictions (no serial hardware)."""

import time
from datetime import datetime

from colorama import Fore, Style, init

from config import BUS_39_STOP, GREEN_LINE_STOP, REFRESH_RATE
from mbta_client import get_predictions

init(autoreset=True)

DIVIDER = " " + "─" * 26

# Rows: (route_id, stop_id, Fore color, short label, destination)
BOARD_ROWS = (
    ("Green-E", GREEN_LINE_STOP, Fore.GREEN, "GL-E", "Heath St"),
    ("39", BUS_39_STOP, Fore.YELLOW, "39", "Forest Hills"),
)


def format_next_arrival(minutes):
    if not minutes:
        return "No service"
    if minutes[0] == 0:
        return "ARR"
    return f"{minutes[0]}min"


def _spaces_before_arrow(plain_label):
    """Pad so `>` lines up with the original layout (1-space prefix + label + spaces = 7)."""
    return max(1, 7 - (1 + len(plain_label)))


def print_board(predictions_by_route):
    now = datetime.now().strftime("%H:%M:%S")

    print(DIVIDER)
    print(DIVIDER)
    for route_id, _, color, label, dest in BOARD_ROWS:
        mins = predictions_by_route[route_id]
        colored = f"{color}{label}{Style.RESET_ALL}"
        pad = " " * _spaces_before_arrow(label)
        print(f" {colored}{pad}> {dest:<12} {format_next_arrival(mins)}")
    print(DIVIDER)
    print(f" Last updated: {now}")


def fetch_predictions():
    return {
        route_id: get_predictions(stop_id, route_id)
        for route_id, stop_id, *_ in BOARD_ROWS
    }


def main():
    while True:
        print_board(fetch_predictions())
        time.sleep(REFRESH_RATE)


if __name__ == "__main__":
    main()
