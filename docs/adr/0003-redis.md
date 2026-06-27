# ADR-0003 — Redis as Distributed Cache and Message Infrastructure

Status: Accepted

Date: 2026-06-27

## Context

ADE-APEX requires a high-performance in-memory system to support distributed caching, temporary state, rate limiting, session storage, distributed locks, and queue coordination.

Persistent transactional data is already handled by PostgreSQL.

## Decision

Redis SHALL be adopted as the primary in-memory data platform.

Redis SHALL be used only for transient and high-speed operational data.

Redis SHALL NOT be treated as the system of record.

## Primary Responsibilities

- Distributed cache
- Queue coordination
- Rate limiting
- Session storage
- Temporary workflow state
- Distributed locking
- Pub/Sub messaging
- Execution coordination

## Data Stored

- Active sessions
- Execution checkpoints
- Queue metadata
- Rate limit counters
- Temporary tokens
- Distributed locks
- Cached API responses

## Data NOT Stored

- User records
- Tenant records
- Workflow definitions
- Audit logs
- Long-term memory
- Knowledge graph

## Rationale

Redis provides:

- Extremely low latency
- High throughput
- Mature clustering
- Replication
- Persistence options
- Pub/Sub support
- Large ecosystem

## Consequences

### Advantages

- Faster response times
- Reduced database load
- Improved scalability
- Better concurrency control

### Trade-offs

- Additional infrastructure
- Cache invalidation complexity
- Memory consumption

## Alternatives Considered

- Memcached
- Hazelcast
- In-process caching

Rejected due to lower flexibility or weaker distributed capabilities.

## Related Contracts

- Queue Manager
- Scheduler
- Event Bus
- Workflow Runtime
- Agent Runtime
