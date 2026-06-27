# ADE-APEX Naming Conventions

Version: 1.0.0

Status: Approved

---

## Purpose

This document defines the official naming conventions used throughout the ADE-APEX platform.

Consistent naming improves readability, discoverability, maintainability, and automation.

---

## General Rules

Names SHALL be:

- Descriptive
- Consistent
- Predictable
- Stable
- Domain-oriented

Avoid:

- Abbreviations unless universally accepted
- Ambiguous names
- Temporary names
- Single-letter identifiers (except loop variables)

---

## Repository

Repository names:

lowercase-with-dashes

Example:

ade-apex-aiops

---

## Directories

Use:

lowercase-with-dashes

Examples:

docs/contracts

docs/architecture

kernel-runtime

---

## Python Packages

Use:

lowercase_with_underscores

Example:

agent_runtime

memory_engine

workflow_runtime

---

## Python Files

snake_case.py

Examples:

agent_runtime.py

workflow_executor.py

policy_engine.py

---

## Classes

PascalCase

Examples:

AgentRuntime

WorkflowEngine

PolicyEvaluator

KnowledgeGraph

---

## Interfaces

Suffix:

Interface

Example:

MemoryInterface

ConnectorInterface

---

## Abstract Classes

Prefix:

Abstract

Example:

AbstractPlugin

AbstractConnector

---

## Functions

snake_case

Examples:

execute_workflow()

publish_event()

load_memory()

validate_policy()

---

## Variables

snake_case

Examples:

tenant_id

workflow_id

agent_context

execution_state

---

## Constants

UPPER_CASE

Examples:

DEFAULT_TIMEOUT

MAX_RETRIES

EVENT_VERSION

---

## Environment Variables

UPPER_CASE

Examples:

DATABASE_URL

REDIS_HOST

OPENAI_API_KEY

JWT_SECRET

---

## REST APIs

Resources use plural nouns.

Examples:

/agents

/workflows

/connectors

/plugins

/events

---

## Event Names

PascalCase

Examples:

WorkflowStarted

WorkflowCompleted

AgentExecuted

PolicyValidated

MemoryUpdated

---

## Database Tables

snake_case

Examples:

workflow_runs

agent_executions

audit_logs

policy_rules

---

## Database Columns

snake_case

Examples:

created_at

updated_at

tenant_id

execution_status

---

## Git Branches

Examples:

feature/kernel-runtime

feature/plugin-sdk

feature/rest-api

bugfix/event-validation

hotfix/security-patch

---

## Git Commit Messages

Format:

type(scope): summary

Examples:

feat(kernel): add workflow scheduler

fix(auth): validate JWT expiration

docs(contracts): update AI Router contract

refactor(memory): simplify cache manager

---

## Version History

1.0.0

Initial Standard
