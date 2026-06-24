#!/usr/bin/env python3
"""Rebuild Appendix A from the canonical source inventory."""

from sync_scaffold import read_inventory, write_source_matrix


def main() -> None:
    records = read_inventory()
    write_source_matrix(records)
    print(f"Wrote Appendix A from {len(records)} source records.")


if __name__ == "__main__":
    main()
