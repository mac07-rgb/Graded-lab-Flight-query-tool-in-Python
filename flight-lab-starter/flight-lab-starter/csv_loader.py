
"""Reading CSV files into flight records and error messages."""

import csv
import os

from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process CSV files and detect duplicate flights."""

    records = []
    errors = []
    seen_flights = set()

    for path in paths:
        filename = os.path.basename(path)

        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)

            # Skip the header (physical line 1)
            next(reader, None)

            for fields in reader:
                line_number = reader.line_num

                # Reconstruct the original row for the error message
                original_line = ",".join(fields)

                # Strip whitespace from every field
                fields = [field.strip() for field in fields]

                # Skip blank lines
                if not fields or all(field == "" for field in fields):
                    continue

                # Skip comment lines
                if fields[0].lstrip().startswith("#"):
                    continue

                # Validate the row
                error_code = validate_row(fields, airports)

                if error_code is not None:
                    errors.append(
                        f"{filename}:{line_number}: {error_code} | {original_line}"
                    )
                    continue

                # Check for duplicate flight ID and departure time
                duplicate_key = (fields[0], fields[3])

                if duplicate_key in seen_flights:
                    errors.append(
                        f"{filename}:{line_number}: DUPLICATE_FLIGHT | {original_line}"
                    )
                    continue

                seen_flights.add(duplicate_key)
                records.append(to_record(fields))

    return records, errors
