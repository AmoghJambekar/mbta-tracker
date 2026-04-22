# MBTA tracker

Small project that polls the [MBTA v3 API](https://www.mbta.com/developers/v3-api) for nearby departures. A **host** machine runs Python: one script prints predictions in the terminal, another sends a compact two-line string to a **Raspberry Pi Pico** over serial for a 16×2 LCD.

## Prerequisites

- Python 3.10+ recommended  
- An [MBTA API key](https://api-v3.mbta.com/register) (free)

## Host setup

Run these from the `host/` directory (that matters for loading `.env`).

```bash
cd host
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `host/.env` with at least:

```bash
MBTA_API_KEY=your_key_here
```

For `tracker.py` only, you can optionally set `SERIAL_PORT` (defaults are in `config.py`).

## Usage

| Script | Purpose |
|--------|---------|
| `python test_api.py` | Colored console board; polls every `REFRESH_RATE` seconds. |
| `python tracker.py` | Fetches the same data and writes `line1|line2\n` to the Pico over serial. |

Stop either script with Ctrl+C.

## Pico firmware

`pico/` contains MicroPython code for an I2C 16×2 display. The host builds each line to 16 characters and separates the two lines with `|`.
