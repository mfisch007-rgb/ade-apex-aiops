# ADR-0006 — Multi-Provider AI Router

Status: Accepted

Date: 2026-06-27

## Context

ADE-APEX must support multiple AI providers while avoiding vendor lock-in. AI capabilities evolve rapidly, and different models excel at different tasks.

The platform requires a unified routing layer capable of selecting providers based on policy, capability, cost, latency, confidence, and availability.

## Decision

ADE-APEX SHALL implement a centralized AI Router.

All LLM requests SHALL pass through the AI Router.

Application services SHALL NOT call AI providers directly.

## Supported Providers

- OpenAI
- Anthropic
- Google Gemini
- Mistral AI
- xAI
- Ollama
- OpenRouter
- Azure OpenAI
- AWS Bedrock
- Future providers through Connector SDK

## Routing Responsibilities

The AI Router SHALL:

- Select the appropriate provider
- Apply routing policies
- Enforce budget limits
- Apply tenant configuration
- Perform fallback routing
- Retry failed requests
- Record metrics
- Publish routing events

## Selection Criteria

Routing decisions MAY consider:

- Model capability
- Cost
- Latency
- Availability
- Confidence score
- Token limits
- Tenant policy
- Regulatory requirements

## Rationale

A centralized routing layer provides:

- Vendor independence
- Lower operational risk
- Better cost optimization
- Consistent security
- Unified observability
- Easier future expansion

## Consequences

### Advantages

- No vendor lock-in
- Centralized governance
- Dynamic model selection
- Better resilience
- Lower long-term maintenance

### Trade-offs

- Additional routing layer
- Increased implementation complexity
- Ongoing provider integration work

## Alternatives Considered

- Direct provider integration
- Single-provider architecture
- Provider-specific services

These were rejected because they reduce flexibility and increase coupling.

## Related Contracts

- AI Router
- Agent Runtime
- Policy Engine
- Connector SDK
- Memory Engine
- Analytics Engine
