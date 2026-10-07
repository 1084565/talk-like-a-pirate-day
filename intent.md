# Pirate Agent

A conversational AI agent with a pirate persona for internal showcase and proof of concept.

## Business challenge

Build a simple AI agent that responds to user messages in a pirate voice and style, demonstrating persona customization capabilities for agents on SAP BTP.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Successful PoC demonstration | — | Agent deployed and responding in pirate style | — | Agent persona customization | user |

## Key Milestones

1. **Agent bootstrapped** — Python A2A agent project created with dependencies.
2. **Pirate persona configured** — System prompt defines pirate speech style and behavior.
3. **Agent responds correctly** — Agent replies to user messages in pirate language.
4. **Agent deployed** — Agent is live and accessible on SAP BTP.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash

### Process Hierarchy

```
Lead to Cash (E2E)
└── Manage Customers and Channels (generic)
    └── Manage customers (generic) (BPS-370)
        └── Manage customer experience
```

### Summary

A pirate-persona conversational agent maps to the customer experience management capability within the Lead to Cash process, enabling personalized AI-driven interactions.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
| ---------------------- | ----------------------- | ---------- | ----------------- | ------------------ | ------------------ | ------------------- | ---- | ------------------- |
| Conversational AI agent with custom persona | None — custom development required | — | — | — | — | — | Yes | No standard SAP product provides a configurable pirate persona agent; custom Python A2A agent is needed |

### Key findings

- No standard SAP product covers the pirate persona use case — custom development is the only path.
- A Python A2A agent on SAP BTP is the right approach: lightweight, deployable, and fully configurable.
- The persona is implemented entirely through the system prompt — no external APIs or MCP tools are required.
- This is a proof-of-concept / internal showcase with no production data or integration requirements.

## Recommendations

### Pirate Persona AI Agent

#### Executive Summary

Custom Python A2A agent with pirate persona via system prompt.

#### Recommended Solution

A pro-code Python agent following the A2A protocol, deployed on SAP BTP. The pirate persona is defined in the system prompt, instructing the LLM to respond exclusively in pirate-style language. No MCP tool integrations are needed for this PoC.

#### Recommended solution category

AI Agent

#### Intent fit
95%
