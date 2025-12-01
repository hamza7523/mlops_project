# Security & Compliance Policy

## 1. Scope

This document describes the security, privacy, and responsible AI practices for the **FloraCare** RAG + LLM system. It covers:
- Prompt injection defenses
- Data privacy & access control
- Dependency vulnerability management
- Guardrails for responsible AI behaviour

## 2. Threat Model (High-Level)

We assume the following potential risks:
- **Prompt injection**: users try to override system instructions, exfiltrate internal docs, or bypass safety policies.
- **Data leakage**: sensitive information from the indexed corpus or user queries gets exposed in responses or logs.
- **Supply-chain risk**: vulnerable Python dependencies (CVEs) in our environment.
- **Abuse of the API**: users attempting harmful, toxic, or disallowed queries.

## 3. Prompt Injection Defenses

We defend against prompt injection at multiple levels:

1. **System prompts & role separation**
   - We define a fixed system prompt that clearly states:
     - The model must follow project rules and not obey user attempts to change them.
     - The model must refuse to reveal internal prompts, credentials, or implementation details.
   - User instructions are always treated as **lower priority** than system rules.

2. **Input validation & sanitization**
   - We apply input validation before calling the LLM:
     - Maximum query length to avoid long, adversarial prompts.
     - Block obvious injection phrases (e.g., “ignore previous instructions”, “you are now…”) via regex / guardrails.
     - Reject or flag queries that attempt to read raw system prompts or configuration.

3. **Retrieval isolation**
   - The retriever only accesses the **approved document corpus**.
   - We never allow users to specify arbitrary file paths, SQL queries, or OS commands.
   - The model only sees retrieved text snippets, not direct access to the underlying storage.

4. **No tool execution from user text**
   - The system does not execute shell commands, database commands, or code directly from user prompts.
   - Any future tool integration must include explicit allow-lists and argument validation.

## 4. Data Privacy & Handling

We handle user and document data as follows:

- **Data minimization**
  - We only ingest documents needed for the RAG use case.
  - We do not store raw user queries or responses longer than necessary for debugging and evaluation.

- **PII & sensitive data**
  - Guardrails/filters run on user input and generated output to detect:
    - Personally Identifiable Information (PII)
    - Highly sensitive content (e.g., medical, financial, or authentication data)
  - If detected, the system can:
    - Mask or redact sensitive fields, or
    - Block and return a safe error message.

- **Access control**
  - Access to environment variables (API keys, DB creds) is restricted to:
    - GitHub Actions secrets
    - Local `.env` files that are NOT committed to Git.
  - No secrets appear in logs, prompts, or example output.

## 5. Dependency Security (pip-audit)

- We manage Python dependencies via `requirements.txt`.
- We run `pip-audit` locally and in CI to detect known CVEs.
- Any build with unresolved vulnerabilities (especially critical ones) is treated as a **failed** CI run.
- The process:
  1. Install/update dependencies.
  2. Run `pip-audit -r requirements.txt --strict`.
  3. Upgrade or pin packages to versions that fix reported CVEs.

## 6. Guardrails & Responsible AI

Our system integrates guardrails to enforce responsible AI behaviour:

- **Input guardrails**
  - Reject or flag prompts that:
    - Request illegal, harmful, or self-harm–related content.
    - Attempt prompt injection or exfiltration of internal system details.
  - These are implemented via guardrails.py in src/app.

- **Output guardrails**
  - Post-process model responses to:
    - Detect toxicity, hate speech, or harassment.
    - Detect hallucinations (e.g., when no relevant context is retrieved).
  - When violations are detected:
    - The system either refuses the request or replaces the answer with a safe, generic message.

- **Logging & monitoring**
  - All guardrail violations are logged with:
    - Timestamp, request ID, rule triggered, and action taken.
  - These logs feed into Prometheus metrics and are visualized in Grafana dashboards.

- **Transparency to users**
  - We clearly communicate limitations:
    - The model may generate inaccurate information.
    - The model does not provide legal, medical, or financial advice.
  - Error / refusal messages explain that responses were blocked due to safety policies.

## 7. Incident Response (High-Level)

If a security or safety issue is discovered (e.g., data leak, bypassed guardrail):

1. Reproduce and isolate the problematic behaviour.
2. Temporarily disable the affected endpoint or feature.
3. Patch:
   - Update guardrail rules and/or prompts.
   - Update dependencies if the issue is CVE-related.
4. Add a regression test so CI ensures the issue does not reappear.

