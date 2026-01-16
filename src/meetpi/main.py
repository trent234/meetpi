#!/usr/bin/env python3

import os
import sys
import time
import secrets
import string
from typing import Optional, Tuple
import jwt  # PyJWT


def getenv_or_fail(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def generate_jwt(room: Optional[str] = None, duration_minutes: int = 10) -> Tuple[str, str]:
    # If no room is provided, generate a random 8-character room name (lowercase letters only).
    if room is None:
        room = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(8))

    secret = getenv_or_fail("JWT_APP_SECRET")
    issuer = getenv_or_fail("JWT_ACCEPTED_ISSUERS")
    audience = getenv_or_fail("JWT_ACCEPTED_AUDIENCES")

    now = int(time.time())
    exp = now + (duration_minutes * 60)

    payload = {
        "iss": issuer,
        "aud": audience,
        "room": room,
        "nbf": now,
        "exp": exp,
        "context": {
            "user": {
                "name": "Guest",
                "moderator": True,
            }
        }
    }

    token = jwt.encode(
        payload,
        secret,
        algorithm="HS256"
    )

    return room, token


def main():
    # Generate a token for a generated room (defaults: 8-char room, 10 minutes)
    room, token = generate_jwt()

    print("\nRoom:")
    print(room)
    print("\nJWT:")
    print(token)
    print("\nJoin URL:")
    print(f"https://meet.trentwilson.com/{room}?jwt={token}")


if __name__ == "__main__":
    main()

