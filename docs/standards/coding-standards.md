# ADE-APEX Coding Standards

Version: 1.0.0

Status: Approved

---

## General Principles

- Readability over cleverness
- Explicit is better than implicit
- Fail fast
- Defensive programming
- SOLID principles
- DRY
- KISS
- YAGNI where appropriate

---

## Naming

Classes:
PascalCase

Functions:
snake_case

Variables:
snake_case

Constants:
UPPER_CASE

Modules:
snake_case

Packages:
lowercase

---

## Python Rules

- Type hints required
- Docstrings required
- Black formatting
- Ruff linting
- Imports sorted
- No wildcard imports

---

## Error Handling

- Never swallow exceptions
- Raise domain-specific exceptions
- Log failures
- Return meaningful errors

---

## Logging

Every service shall log:

- startup
- shutdown
- warnings
- errors
- retries
- performance

---

## Testing

Minimum coverage:

90%

Required:

- unit tests
- integration tests
- contract tests

---

## Security

Never:

- hardcode secrets
- expose credentials
- disable authentication
- bypass authorization

---

## Performance

Target latency:

REST:
<150 ms

Internal API:
<50 ms

Event publishing:
<10 ms

---

Version History

1.0.0

Initial Standard
