
"""Running queries against the flight database."""

import re
from datetime import datetime


RECORD_KEYS = {
    "flight_id",
    "origin",
    "destination",
    "departure_datetime",
    "arrival_datetime",
    "price",
}

STRING_KEYS = {
    "flight_id",
    "origin",
    "destination",
}

DATETIME_KEYS = {
    "departure_datetime",
    "arrival_datetime",
}

NUMERIC_KEYS = {
    "price",
    "min_price",
}

QUERY_KEYS = (
    STRING_KEYS
    | DATETIME_KEYS
    | NUMERIC_KEYS
    | {"sort_by", "order", "limit"}
)


def valid_datetime(value):
    if not isinstance(value, str):
        return False

    if not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}",
        value
    ):
        return False

    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def valid_query(query):
    if not isinstance(query, dict):
        return False

    # Reject unknown keys
    if any(key not in QUERY_KEYS for key in query):
        return False

    # String conditions
    for key in STRING_KEYS:
        if key in query and not isinstance(query[key], str):
            return False

    # Datetime conditions
    for key in DATETIME_KEYS:
        if key in query and not valid_datetime(query[key]):
            return False

    # Numeric conditions (booleans are not accepted)
    for key in NUMERIC_KEYS:
        if key in query:
            value = query[key]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False

    # Sorting
    if "sort_by" in query:
        if not isinstance(query["sort_by"], str):
            return False

        if query["sort_by"] not in RECORD_KEYS:
            return False

    # Order
    if "order" in query:
        if query["sort_by"] is None if "sort_by" in query else True:
            return False

        if query["order"] not in ("asc", "desc"):
            return False

    # Limit
    if "limit" in query:
        limit = query["limit"]

        if isinstance(limit, bool) or not isinstance(limit, int):
            return False

        if limit < 0:
            return False

    return True


def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object."""

    if not valid_query(query):
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": []
        }

    matches = []

    for flight in db:
        matched = True

        for key in STRING_KEYS:
            if key in query and flight[key] != query[key]:
                matched = False
                break

        if not matched:
            continue

        if (
            "departure_datetime" in query
            and flight["departure_datetime"] < query["departure_datetime"]
        ):
            continue

        if (
            "arrival_datetime" in query
            and flight["arrival_datetime"] > query["arrival_datetime"]
        ):
            continue

        if "price" in query and flight["price"] > query["price"]:
            continue

        if "min_price" in query and flight["price"] < query["min_price"]:
            continue

        matches.append(flight)

    # Sort if requested. Python sorting is stable.
    if "sort_by" in query:
        sort_key = query["sort_by"]
        reverse = query.get("order", "asc") == "desc"

        matches = sorted(
            matches,
            key=lambda flight: flight[sort_key],
            reverse=reverse
        )

    # Apply limit after sorting
    if "limit" in query:
        matches = matches[:query["limit"]]

    return {
        "query": query,
        "matches": matches
    }


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of query objects."""

    if isinstance(queries, dict):
        queries = [queries]

    if not isinstance(queries, list):
        queries = [queries]

    return [run_query(db, query) for query in queries]
