# Plugin Runtime Directory Layout

Version: 1.0.0

## Purpose

Defines the canonical filesystem structure for the Plugin Runtime subsystem.

No implementation should deviate from this layout without an approved Architecture Decision Record (ADR).

---

app/kernel/plugins/

├── __init__.py
├── manager.py
├── registry.py
├── loader.py
├── validator.py
├── metadata.py
├── lifecycle.py
├── context.py
├── configuration.py
├── sandbox.py
├── health.py
├── exceptions.py
├── discovery.py
├── dependency.py
└── interfaces.py

---

tests/unit/kernel/plugins/

manager_test.py

registry_test.py

loader_test.py

validator_test.py

lifecycle_test.py

health_test.py

---

docs/engineering/packs/002-plugin-runtime/

README.md

ARCHITECTURE.md

CONTRACTS.md

INTERFACES.md

DIRECTORY_LAYOUT.md

IMPLEMENTATION_PLAN.md

VALIDATION.md

RELEASE_NOTES.md

---

Design Rules

One responsibility per module.

No circular dependencies.

Kernel owns lifecycle.

Plugins never modify Kernel internals.

Contracts remain implementation independent.

Git remains the source of truth.

---

Status

Directory Layout Approved Pending Review.
