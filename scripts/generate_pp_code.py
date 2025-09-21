#!/usr/bin/env python3
"""Generate PP identifiers based on UUID4 entropy.

The script emits codes shaped like ``PP-<hex>``. It grabs a UUID4, which
provides 128 bits of randomness, and slices the first 16 hexadecimal
characters (64 bits). That yields around 1 in 190 billion collision
risk even after ~14k identifiers, matching this PP naming scheme.
"""

import uuid

def main() -> None:
    """Print a new PP code with the agreed 16-hex suffix."""
    code = f"PP-{uuid.uuid4().hex[:16]}"
    print(code)

if __name__ == "__main__":
    main()
