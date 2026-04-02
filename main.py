#!/usr/bin/env python3
"""BiSHunter - TBC Classic gear optimization tool.

Parses AskMrRobot exports and cross-references against the TBC item database
to tell you what gear to keep, what to vendor, and what to farm next.
"""

import sys
import config
from db_loader import load_db
from amr_parser import parse_amr_export, format_equipped
from recommender import format_report


def main():
    # Allow passing AMR export string as CLI argument
    if len(sys.argv) > 1:
        amr_string = sys.argv[1]
    else:
        amr_string = config.AMR_EXPORT

    print("=" * 70)
    print("  BiSHunter - TBC Classic Gear Advisor")
    print("=" * 70)
    print()

    # Parse AMR export
    print("Parsing AskMrRobot export...")
    data = parse_amr_export(amr_string)
    char = data["character"]
    print(f"  Character: {char['name']} - Level {char['level']} {char['class']}")
    print(f"  Server:    {char['region']}-{char['server']} ({char['faction']})")
    print(f"  Main Spec: {config.CHARACTER['main_spec'].upper()}")
    print(f"  Off Spec:  {config.CHARACTER['off_spec'].upper()}")
    print()

    # Load item database
    print("Loading TBC item database...")
    conn = load_db(config.DB_PATH)
    print()

    # Generate report
    report = format_report(
        conn,
        data["equipped"],
        data["inventory"],
        config.CHARACTER["main_spec"],
        config.CHARACTER["off_spec"],
    )
    print(report)

    conn.close()


if __name__ == "__main__":
    main()
