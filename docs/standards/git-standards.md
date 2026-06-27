# ADE-APEX Git Standards

Version: 1.0.0

Status: Approved

---

## Purpose

This document defines the official Git workflow for ADE-APEX development.

All contributors SHALL follow these standards to maintain repository integrity, code quality, and traceability.

---

## Branch Strategy

Permanent branches:

- main
- develop

Working branches:

- feature/*
- bugfix/*
- hotfix/*
- release/*

Examples:

feature/kernel-runtime

feature/agent-runtime

bugfix/event-validation

hotfix/authentication

---

## Development Workflow

Every feature SHALL follow:

develop

↓

feature/<feature-name>

↓

Commit frequently

↓

Push feature branch

↓

Pull Request

↓

Code Review

↓

Merge into develop

↓

Release branch

↓

main

---

## Commit Message Format

Pattern:

type(scope): summary

Examples:

feat(kernel): add workflow runtime

feat(router): support OpenAI routing

fix(auth): validate JWT expiration

docs(contracts): update scheduler contract

refactor(memory): simplify cache layer

test(api): add integration tests

chore(ci): update GitHub Actions

---

## Commit Types

- feat
- fix
- docs
- refactor
- test
- perf
- build
- ci
- chore

---

## Pull Requests

Every Pull Request SHALL include:

- Summary
- Motivation
- Design impact
- Testing performed
- Related issue
- Reviewer

---

## Code Reviews

Every review SHALL verify:

- Architecture compliance
- Contract compliance
- Security
- Performance
- Testing
- Documentation

---

## Branch Protection

The following branches SHALL be protected:

- main
- develop

Direct pushes are prohibited.

Changes SHALL be merged through Pull Requests.

---

## Merge Strategy

Preferred:

Squash Merge

Allowed:

Merge Commit

Avoid:

Rebase merges on shared branches.

---

## Tagging

Release tags:

v1.0.0

v1.1.0

v2.0.0

---

## Release Process

1. Complete development
2. Merge into develop
3. Run CI/CD
4. Create release branch
5. Final validation
6. Merge into main
7. Tag release
8. Publish artifacts

---

## Repository Hygiene

Delete merged feature branches.

Keep commit history clean.

Avoid force pushes.

Never commit secrets.

---

## Version History

1.0.0

Initial Standard
