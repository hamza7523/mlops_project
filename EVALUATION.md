### Milestone-2 Evaluation Report — Prompt Engineering, RAG, Guardrails & Monitoring

---

## 1. Overview
This report summarizes all evaluations completed for Milestone-2: Operationalizing LLMs.  
The project includes:

- Three prompt strategies  
- A reproducible evaluation pipeline using TinyLlama GGUF  
- ROUGE-L scoring  
- MLflow experiment tracking  
- RAG pipeline evaluation  
- Monitoring & guardrails  

All strategies were evaluated using:

```bash
python experiments/run_eval.py <strategy>
```

---

## 2. Evaluation Dataset
The held-out dataset used for evaluation is located at:

```
data/eval.jsonl
```

Each record contains:
- `question`
- `context_class`
- `ideal_answer`

This dataset is **never** used during prompt creation or tuning.

---

## 3. Prompting Strategies Evaluated

All prompt scripts exist in the folder:

```
experiments/prompts/
```

---

### 3.1 Zero-Shot Prompting
**File:** `zero_shot.py`

**Characteristics:**
- No examples  
- Minimal instructions  
- Uses context_class only if provided  

**Template:**
```
You are an AI assistant for plant disease detection.
The user has a plant with the following condition: {context_class}.

Question: {question}

Answer:
```

---

### 3.2 Few-Shot Prompting (k=3)
**File:** `few_shot.py`

Includes real examples of:
- Apple Scab  
- Tomato Early Blight  
- Healthy Corn  

This approach improves consistency and treatment recommendations.

---

### 3.3 Meta-Prompt / Persona Prompting
**File:** `meta_prompt.py`

Defines persona:  
**Dr. Flora — Plant Pathologist with 20 years experience**

Includes:
- Persona  
- Rules  
- Objectives  
- Structured response format:

```
- Diagnosis: [Disease Name]
- Advice: [Actionable Steps]
```

This is the **most structured and reliable** prompt template.

---

## 4. Evaluation Pipeline

`run_eval.py` performs the following steps:

1. Loads TinyLlama `gguf` model from `backend/models/`  
2. Builds prompts using the selected strategy  
3. Runs inference  
4. Computes **ROUGE-L F-measure** via `rouge_scorer`  
5. Logs parameters + metrics using MLflow  
6. Saves generated CSV to:

```
experiments/results/results_<strategy>.csv
```

MLflow experiment name:

```
Flora_Prompt_Engineering
```

---

## 5. Quantitative Results (From CSV Outputs)

### 5.1 Average ROUGE-L Scores

| Strategy | Avg ROUGE-L | Notes |
|----------|-------------|-------|
| Zero-Shot | ~0.148 | Weak grounding; inconsistent answers |
| Few-Shot | ~0.305 | More stable; clearer diagnosis |
| Meta-Prompt | **~0.342** | Best factual accuracy + structure |

**Meta-Prompt** produced the strongest performance overall.

---

## 6. Qualitative Observations

### Zero-Shot
- Answers are generic  
- Misdiagnoses occur frequently  
- Lacks actionable advice  

### Few-Shot
- Better structure due to examples  
- More accurate disease identification  
- Fewer hallucinations  

### Meta-Prompt
- Most consistent and reliable  
- Strong factual grounding  
- Clear diagnosis + treatment formatting  

---

## 7. Why Meta-Prompt Outperformed Others

- Persona reduces randomness  
- Rules prevent hallucinations  
- Format improves ROUGE matching  
- Domain identity enhances correctness  

**Ranking: Meta-Prompt > Few-Shot > Zero-Shot**

---

## 8. RAG Pipeline Evaluation

RAG pipeline (from `backend/app.py`) was evaluated separately.

### Key Findings:
- Retrieval adds factual grounding beyond any prompt-only method  
- RAG + Meta-Prompt yields the best practical results  
- Hallucination rate drops significantly  

RAG is the most reliable approach when context is required.

---

## 9. Guardrails Evaluation

Guardrails included:
- Prompt injection defense  
- PII detection  
- Toxicity moderation  
- Hallucination filtering  

Logged via:
```
metrics_server.py
```

### Outcome:
- Prevented unsafe responses  
- Never blocked valid queries  
- Provided safer real-world deployment behavior  

---

## 10. Monitoring & Observability

### Prometheus Metrics Captured:
- Latency  
- Token usage  
- Cost estimation  
- Guardrail violations  

### Grafana Visualization:
- Throughput graphs  
- Retrieval latency patterns  
- Error spikes  
- Token usage per strategy  

### EvidentlyAI Drift Detection:
- No significant drift in dataset detected  

---

## 11. Final Insights

1. Meta-Prompt produces the strongest standalone prompting strategy  
2. RAG further improves factual accuracy substantially  
3. Zero-shot is insufficient for agricultural diagnosis tasks  
4. Monitoring is essential for real deployment  
5. Guardrails significantly increase safety  

---

## 12. Conclusion

This milestone successfully demonstrates:

- Structured prompt engineering  
- Quantitative (ROUGE-L) + qualitative analysis  
- MLflow experimental tracking  
- Retrieval-Augmented Generation  
- Guardrails for safe output  
- Monitored LLM pipeline using Prometheus + Grafana  
- Drift detection using EvidentlyAI  

**Meta-Prompt performed best among prompt strategies, while RAG produced the highest factual correctness overall.**
