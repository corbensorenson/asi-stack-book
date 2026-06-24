#!/usr/bin/env python3
"""Rebuild Appendix A from the canonical source inventory and book structure."""

from sync_scaffold import read_inventory, read_structure, write_source_matrix


def main() -> None:
    records = read_inventory()
    structure = read_structure()
    write_source_matrix(records, structure)
    print(f"Wrote Appendix A from {len(records)} source records.")


if __name__ == "__main__":
    main()
