
"""Flight Schedule Parser and Query Tool - command-line entry point."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


# Student details
STUDENT_ID = "251ADB003"
FIRST_NAME = "Mohammad"
LAST_NAME = "Anas"


def main(argv: list[str] | None = None) -> int:
    """Run the program and return exit code 0, 1 or 2."""

    parser = argparse.ArgumentParser(
        description="Flight Schedule Parser and Query Tool"
    )

    source = parser.add_mutually_exclusive_group(required=True)

    source.add_argument("-i", metavar="FILE")
    source.add_argument("-d", metavar="FOLDER")
    source.add_argument("-j", metavar="FILE")

    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", metavar="FILE")
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", metavar="FOLDER", default=".")

    # Parse command-line arguments
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    # Check usage restrictions
    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")

    if args.j and args.a:
        pass  # -a is ignored with -j

    if args.j and args.o is not None:
        parser.error("-o cannot be used with -j")

    if args.o is not None and not (args.i or args.d):
        parser.error("-o can only be used with -i or -d")

    db_output = args.o or "db.json"

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)

    handler = None

    try:
        # -------------------------------------------------
        # MODE 1: Read CSV files
        # -------------------------------------------------
        if args.i or args.d:

            if args.i:
                paths = [args.i]

            else:
                if not os.path.isdir(args.d):
                    raise OSError(
                        f"Folder does not exist: {args.d}"
                    )

                paths = sorted(
                    os.path.join(args.d, name)
                    for name in os.listdir(args.d)
                    if name.endswith(".csv")
                    and os.path.isfile(
                        os.path.join(args.d, name)
                    )
                )

                if not paths:
                    raise OSError(
                        f"No CSV files found in folder: {args.d}"
                    )

            # Load airport codes
            airports = load_airports(args.a)

            # Prepare errors.log beside the database
            output_dir = os.path.dirname(
                os.path.abspath(db_output)
            )

            log_path = os.path.join(
                output_dir,
                "errors.log"
            )

            handler = logging.FileHandler(
                log_path,
                mode="w",
                encoding="utf-8"
            )

            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            )

            logger.addHandler(handler)

            # Process CSV files
            records, errors = parse_files(
                paths,
                airports
            )

            # Save JSON database
            with open(
                db_output,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    records,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            # Write invalid rows using logging
            for error in errors:
                logger.warning("%s", error)

            print(f"Valid flights: {len(records)}")
            print(f"Invalid rows: {len(errors)}")

        # -------------------------------------------------
        # MODE 2: Load an existing JSON database
        # -------------------------------------------------
        else:

            with open(
                args.j,
                "r",
                encoding="utf-8"
            ) as file:
                records = json.load(file)

            if not isinstance(records, list):
                raise ValueError(
                    "JSON database must be an array of objects"
                )

            if not all(
                isinstance(record, dict)
                for record in records
            ):
                raise ValueError(
                    "JSON database must contain objects"
                )

            print(f"Loaded flights: {len(records)}")

        # -------------------------------------------------
        # MODE 3: Run queries
        # -------------------------------------------------
        if args.q:

            with open(
                args.q,
                "r",
                encoding="utf-8"
            ) as file:
                queries = json.load(file)

            if not isinstance(queries, (dict, list)):
                raise ValueError(
                    "Query file must contain an object or array"
                )

            if not os.path.isdir(args.r):
                raise OSError(
                    f"Response folder does not exist: {args.r}"
                )

            responses = run_queries(
                records,
                queries
            )

            # Generate response filename
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M"
            )

            response_name = (
                f"response_{STUDENT_ID}_"
                f"{FIRST_NAME}_{LAST_NAME}_"
                f"{timestamp}.json"
            )

            response_path = os.path.join(
                args.r,
                response_name
            )

            # Save query responses
            with open(
                response_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    responses,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            print(
                f"Query response saved: {response_path}"
            )

        return 0

    except (
        OSError,
        ValueError,
        json.JSONDecodeError,
        UnicodeError
    ) as exc:

        print(
            f"Error: {exc}",
            file=sys.stderr
        )

        return 1

    finally:
        # Always remove and close the logging handler
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
