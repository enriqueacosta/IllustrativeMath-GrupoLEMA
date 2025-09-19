#!/usr/bin/env python3
"""Generate a unique PP code identifier."""

import uuid

def main() -> None:
    code = f"PP-{uuid.uuid4().hex[:16]}"
    print(code)

if __name__ == "__main__":
    main()
