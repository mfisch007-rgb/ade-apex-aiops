# Kernel Contract 03 — Workflow Runtime

Version: 1.0.0

Status: Approved

---

## Purpose

Executes workflow definitions.

Coordinates tasks.

Maintains workflow state.

Supports retries.

Supports resumable execution.

---

## States

Created

Queued

Running

Waiting

Completed

Cancelled

Failed

---

## Responsibilities

- Execute workflow
- Retry failures
- Emit events
- Save checkpoints
- Recover after restart

