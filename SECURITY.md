# SECURITY & RESPONSIBLE AI POLICY

This document outlines the security, privacy, and responsible-AI protections implemented in the **RAG-Based LLM System** for the MLOps course project. It covers prompt-injection defenses, PII and data privacy rules, safety guardrails, and dependency security through automated vulnerability scanning.

---

## 1. Threat Model Overview

The system assumes the following risks:

- Users attempting **prompt injection** to bypass system instructions or extract internal details.
- **Data leakage**, including accidental exposure of sensitive documents or returned PII.
- **Model misuse**, including attempts to generate harmful, unsafe, or disallowed content.
- **Dependency vulnerabilities** in the Python ecosystem (CVEs).
- **Hallucinations** caused by retrieval mismatch or missing context.

Security is enforced both through **guardrails** and **system-level protections**.

---

## 2. Prompt Injection Defenses

To prevent users from tampering with system behaviour or revealing internal prompts:

### **2.1 System-Prompt Isolation**
- A fixed system prompt defines non-negotiable rules.
- User messages never override system-level policies.

### **2.2 Input Sanitization**
- The pipeline scans queries for common injection attempts:
  - “Ignore previous instructions”
  - “You are now…”
  - Attempts to extract system prompts
- Suspicious inputs trigger a safe refusal response.

### **2.3 Retrieval Isolation**
- The user cannot modify what documents are retrieved.
- The model only sees context passed via the retriever.
- No direct file access, shell commands, or code execution are allowed.

### **2.4 No Arbitrary Tool Execution**
- User text can never trigger unsafe functions, external tools, or system commands.

---

## 3. Data Privacy Guidelines

We enforce strict data-handling and privacy rules:

### **3.1 Data Minimization**
- Only course-approved documents are indexed.
- No raw user queries or model outputs are stored permanently.

### **3.2 No Logging of Sensitive Data**
- Logs avoid storing:
  - API keys  
  - Credentials  
  - PII  
  - Raw model responses containing sensitive data  

### **3.3 Environment Variable Safety**
- All secrets are loaded via:
  - `.env` (ignored by Git)
  - GitHub Actions secrets  
- No secrets appear in prompts, sample outputs, or logs.

### **3.4 Access Control**
- Only project team members can access ingestion scripts or deployment environments.

---

## 4. PII (Personally Identifiable Information) Policies

The model must not generate or expose sensitive personal information.

### **4.1 Input PII Protection**
- Inputs are scanned for PII types such as:
  - Email, address, phone number
  - Government ID numbers
- If users provide PII, the system refuses to return or store it.

### **4.2 Output PII Protection**
- Guardrails block the model from:
  - Fabricating PII about real individuals
  - Returning sensitive content found in the indexed corpus
- Sensitive fields may be redacted or masked.

### **4.3 PII in Retrieval**
- Documents containing PII are excluded from ingestion.

---

## 5. Safety Guardrail Architecture

Our system implements **multi-layered safety**:

### **5.1 Input Guardrails**
- Detect harmful intents:
  - Violence  
  - Hate content  
  - Self-harm  
  - Illegal activities  
- On detection → The system blocks the query and returns a safe response.

### **5.2 Output Guardrails**
- After model generation, output passes through:
  - Toxicity filters  
  - Safety classifiers  
  - QA checks for hallucinations  

If safety violations occur:
- The system modifies or blocks the output.
- A transparent message is returned to the user explaining the restriction.

### **5.3 RAG Hallucination Controls**
- If retrieved context has low relevance, the system:
  - Warns the user  
  - Falls back to safe refusal  
  - Does not hallucinate authoritative answers  

### **5.4 Monitoring**
- Guardrail events (blocked inputs, redacted PII, etc.) are recorded for evaluation.

---

## 6. Dependency & Supply-Chain Security (pip-audit)

To identify vulnerabilities in Python libraries:

### **6.1 pip-audit Integration**
- We run:

```bash
pip-audit -r requirements.txt --strict



