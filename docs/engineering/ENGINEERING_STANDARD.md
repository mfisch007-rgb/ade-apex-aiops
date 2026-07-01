# ADE-APEX Engineering Standard

Version: 1.0

## Purpose

This document defines the mandatory engineering workflow for every subsystem developed within ADE-APEX.

The objective is consistency, reviewability, reproducibility and safe autonomous development.

---

# Engineering Pipeline

Every subsystem MUST follow this exact sequence.

Phase A
AI generates complete subsystem.

↓

Phase B
Architecture Review

↓

Phase C
Consistency Review

↓

Phase D
Generate one guarded Termux payload

↓

Phase E
Execute payload

↓

Phase F
Run validation

↓

Phase G
Commit

No phase may be skipped.

---

# Definition of Done

A subsystem is complete only when it includes:

Architecture

Contracts

Implementation

Tests

Documentation

Migration notes (if applicable)

Validation commands

Commit message

---

# Guard Rule

Every executable payload MUST begin with:

cd ~/ade-apex-aiops || exit 1

No exceptions.

---

# Repository Rule

Git is the single source of truth.

Generated code is never considered authoritative until committed.

---

# Kernel First

Everything must integrate through the Kernel.

No subsystem may bypass kernel contracts.

---

# Engineering Packs

Future work is delivered only as Engineering Packs.

Never as isolated files.
