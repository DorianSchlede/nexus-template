# D8: Framework & LLM Lock-In Concerns

**Type**: Desirability
**Importance**: 8/10 (HIGH - Product requirement)
**Evidence**: Assumption
**Status**: New for v2.0 (added based on BMC v3.0 BYOM strategy)
**Version**: 2.0

---

## Hypothesis

**We believe** AI agent developers fear vendor lock-in and strongly prefer solutions that work across frameworks (LangGraph, Mastra, Langchain, Letta), LLM providers (OpenAI, Anthropic, local models), Observability Frameworks and Evaluation Frameworks with **BYOM (Bring Your Own Model)** as a must-have requirement.

**We'll know when** 15+ out of 20 interviewed developers confirm:
- Currently use or plan to use multiple frameworks/LLM providers
- Rate "framework-agnostic" as 8+/10 importance
- Would NOT adopt solution that locks them into one framework or LLM
- Specific concern about switching costs or provider pricing changes
- Strong preference for **BYOM** over platform-provided inference

**Why it matters**: If true, framework/LLM agnosticism + BYOM are strong differentiators and product requirements. If false, we can focus on 1-2 primary frameworks/LLMs and reduce complexity.

---

## Links to Business Model

**Linked to:**
- **VPC v2.0**: Gain "Framework freedom + LLM decoupling"
- **VPC v2.0**: Gain Creator "BYOLLM support"
- **BMC v3.0**: Value Proposition #5 "Works with Your Stack"
- **BMC v3.0**: Value Proposition #5 "BYOM (Bring Your Own Model)"
- **BMC v3.0**: Cost Structure "BYOM Model eliminates LLM COGS risk"

---

## Current Evidence

**Evidence Level**: Assumption (needs validation with multi-framework users)

---

## Test Cards

**Related Tests**:
- [[1-customer-discovery-interviews-TEST-CARD]] (Multi-hypothesis customer interviews)
- [[2-byom-architecture-TEST]] (F3 - Technical validation)

---

**Generated**: 2025-10-26 (v2.0 Strategic Refinement)
**Framework**: Testing Business Ideas - Desirability Hypothesis
