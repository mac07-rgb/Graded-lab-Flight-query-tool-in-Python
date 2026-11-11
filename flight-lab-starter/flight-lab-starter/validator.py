
"""Row validation: airport list loading, single-row checks, record building."""

import re
import math
from datetime import datetime


def load_airports(path: str) -> set[str]:
    airports = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            code = line.strip()

            if code and not code.startswith("#"):
                airports.add(code)

    return airports


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    # Check 1: exactly six fields
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    fields = [field.strip() for field in fields]

    flight_id, origin, destination, departure, arrival, price = fields

    # Check 2: no empty fields
    if any(field == "" for field in fields):
        return "MISSING_FIELD"

    # Check 3: flight ID must contain 2-8 ASCII letters/digits
    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id):
        return "INVALID_FLIGHT_ID"

    # Check 4: valid origin
    if not re.fullmatch(r"[A-Z]{3}", origin) or origin not in airports:
        return "INVALID_ORIGIN"

    # Check 5: valid destination
    if not re.fullmatch(r"[A-Z]{3}", destination) or destination not in airports:
        return "INVALID_DESTINATION"

    # Check 6: origin and destination cannot be the same
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"

    # Check 7: departure datetime
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", departure):
        return "INVALID_DEPARTURE"

    try:
        departure_time = datetime.strptime(departure, "%Y-%m-%d %H:%M")
    except ValueError:
        return "INVALID_DEPARTURE"

    # Check 8: arrival datetime
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", arrival):
        return "INVALID_ARRIVAL"

    try:
        arrival_time = datetime.strptime(arrival, "%Y-%m-%d %H:%M")
    except ValueError:
        return "INVALID_ARRIVAL"

    # Check 9: arrival must be later than departure
    if arrival_time <= departure_time:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    # Check 10: price must be a finite number
    try:
        numeric_price = float(price)
    except ValueError:
        return "INVALID_PRICE"

    if not math.isfinite(numeric_price):
        return "INVALID_PRICE"

    # Check 11: price must be positive
    if numeric_price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    fields = [field.strip() for field in fields]

    return {
        "flight_id": fields[0],
        "origin": fields[1],
        "destination": fields[2],
        "departure_datetime": fields[3],
        "arrival_datetime": fields[4],
        "price": float(fields[5])
    }
