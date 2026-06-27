# ADR-0002 — PostgreSQL as Primary Relational Database

Status: Accepted

Date: 2026-06-27

## Context

ADE-APEX requires a transactional database capable of supporting multi-tenancy, ACID compliance, high availability, indexing, JSON storage, and mature ecosystem support.

The platform stores workflow metadata, users, tenants, audit logs, policies, configuration, analytics metadata, and operational records.

## Decision

PostgreSQL SHALL be the primary relational database for ADE-APEX.

All transactional business data SHALL be stored in PostgreSQL.

Application services SHALL access PostgreSQL through repository abstractions rather than direct SQL embedded throughout the codebase.

## Rationale

PostgreSQL provides:

- ACID transactions
- Excellent performance
- Mature replication support
- Rich indexing
- Native JSONB
- Full-text search
- Strong security
- Large ecosystem
- Long-term stability

## Consequences

### Advantages

- Reliable transactions
- Excellent scalability
- Flexible schema evolution
- Strong tooling
- Enterprise adoption

### Trade-offs

- Operational complexity
- Database administration requirements
- Migration management

## Alternatives Considered

- MySQL
- MariaDB
- SQLite
- MongoDB as primary datastore

These were rejected because they either lack required transactional guarantees, advanced querying capabilities, or enterprise operational maturity.

## Related Contracts

- Tenant Manager
- Authentication
- Authorization
- Analytics Engine
- Memory Engine
