# AGENTS.md

## Purpose

This program is a **minimal JWT issuer for Jitsi meetings**.

It generates **one JWT per room** and is intended for **simple, time-bound meetings** where:
- All participants use the same link
- Entry is allowed only during a short join window
- The meeting cannot be rejoined after it ends

There is **no user management**, **no persistence**, and **no runtime control of Jitsi**.

---

## Core Model

### Room
- A room is identified solely by its **name** (string).
- Rooms are **not created or stored** anywhere.
- A room exists only when users join it in Jitsi.

### Token
- One JWT is generated **per room**.
- The JWT:
  - Authorizes joining **exactly one room**
  - Is valid only for a **short time window**
  - Grants **moderator privileges** to all participants

### Active Room
- An “active room” is defined as:
  - A room whose JWT has **not yet expired**

There is no concept of presence, state, or tracking.

---

## Security & Trust Model

### Authority
- Jitsi (via Prosody) is the **only authority** that validates tokens.
- This program’s sole responsibility is to:
  - Mint correctly signed JWTs
  - With correct claims

### Enforcement
- JWT expiration (`exp`) is enforced **only at join time**
- Participants are **not auto-kicked** when tokens expire
- Ending a meeting destroys the conference instance
- Expired tokens prevent **rejoining**

---

## Assumptions

This program assumes:

- JWT authentication is enabled in Jitsi
- `AUTH_TYPE=jwt` is configured
- HS256 signing is used
- All participants are trusted to join on time

No attempt is made to:
- Revoke tokens early
- Track users
- Prevent token sharing

---

## Required Environment Variables

The program **must not hardcode secrets**.

Required:

- `JWT_APP_SECRET`  
  Shared secret used to sign tokens (HS256)

- `JWT_ACCEPTED_ISSUERS`  
  Must match Jitsi’s `JWT_ACCEPTED_ISSUERS`

- `JWT_ACCEPTED_AUDIENCES`  
  Must match Jitsi’s `JWT_ACCEPTED_AUDIENCES`

---

## JWT Claims Used

Mandatory claims:

- `iss` — issuer
- `aud` — audience
- `room` — exact room name
- `nbf` — not before (now)
- `exp` — expiration (join window)

Context claims:

- `context.user.moderator = true`
- `context.user.name` (optional, cosmetic)

No other claims are required.

---

## Token Lifetime Strategy

This program intentionally uses a **short expiration** relative to meeting length.

Example:
- Meeting duration: 60 minutes
- JWT expiration: 5–10 minutes after start

Effects:
- All participants must join on time
- Tokens expire while the meeting continues
- After the meeting ends, rejoin is impossible

This is **by design**.

---

## Non-Goals

This program explicitly does NOT:

- Create user-specific tokens
- Maintain a database
- Track active meetings
- Interact with Jicofo or Prosody at runtime
- Enforce meeting end times
- Provide a UI (beyond printing a URL)

Any such features should be added in a **separate, higher-level service**.

---

## Extension Guidance

If extending this program, prefer:
- Adding optional flags (duration, moderator)
- Adding minimal persistence (optional)
- Keeping JWT issuance stateless

Avoid:
- Runtime coupling to Jitsi internals
- Long-lived tokens
- Session tracking

---

## Summary

This program is intentionally small.

Its job is simple:
> **Create a short-lived capability token that allows joining exactly one Jitsi room.**

Anything beyond that is outside its scope.
  

