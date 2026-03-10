#!/usr/bin/env python3
"""Generate PP identifiers based on UUID4 entropy.

The script emits codes shaped like ``PP-<hex>``. It grabs a UUID4, which
provides 128 bits of randomness, and slices the first 16 hexadecimal
characters (64 bits). That yields around 1 in 190 billion collision
risk even after ~14k identifiers, matching this PP naming scheme.
"""

import uuid


def new_pp_id() -> str:
    """Return a fresh PP identifier (e.g. ``PP-a3f1...``).

    Grabs a UUID4 and slices the first 16 hexadecimal characters (64 bits),
    yielding around 1 in 190 billion collision risk even after ~14k identifiers.
    """
    code = uuid.uuid4().hex[:16]
    return f"PP-{code}"


def main() -> None:
    """Print a new PP id and the corresponding filename."""
    xml_id = new_pp_id()
    print(xml_id)
    print(f"Filename is: {xml_id}.ptx")

if __name__ == "__main__":
    main()
