# iyuno-agent-portfolio

> AI Agent portfolio project aligned to the Iyuno AI Agent Engineer job posting (course assignment, September 2026).

## 1. What this project proves

This repository turns job-posting requirements into runnable evidence:

| Job requirement | Evidence in this repo |
|---|---|
| LLM-based AI Agent design/development | `agent/router.py`, `agent/rag.py`, `app/main.py` |
| RAG search + answer with citations | `agent/rag.py`, `data/docs/`, `/ask` |
| Tool calling | `agent/tools.py` (calculator, policy lookup, source search) |
| API / multi-step workflow | `agent/router.py`, FastAPI endpoints |
| Evaluation / feedback loop | `evaluation/evaluate.py`, `evaluation/metrics.json`, `agent/feedback.py` |
| Latency / reliability / cost awareness | evaluation metrics + request timing + token/cost estimate |
| Tests / reproducibility | `tests/`, GitHub Actions CI |

## 2. Architecture

User question -> Router -> RAG Retriever -> Tools/API -> Answer + citations + feedback
                                  -> evaluation logs: hit@k, faithfulness, latency, token cost

## 3. Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python -m agent.ingest
python -m evaluation.evaluate
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

### Example

```bash
curl -X POST http://127.0.0.1:8000/ask   -H "Content-Type: application/json"   -d '{"question":"What is the principle of least privilege and which source supports it?"}'
```

## 4. RAG pipeline

1. Load Markdown source notes from `data/docs/`.
2. Split into chunks.
3. Build TF-IDF vectors (offline, reproducible baseline).
4. Rank chunks by cosine similarity.
5. Return answer plus source IDs/URLs.
6. Log latency and estimated token usage.

The retriever is deliberately dependency-light. A production version can swap the vectorizer for a hosted embedding model/vector DB without changing the API contract.

## 5. Tool calling

The router can select:
- `calculator`: arithmetic expressions
- `policy_lookup`: deterministic lookup over `data/policies.json`
- `source_search`: search source metadata

Tool calls are recorded in the response trace.

## 6. Evaluation

The included evaluation set has 30 questions. Run:

```bash
python -m evaluation.evaluate
```

Outputs:
- `evaluation/metrics.json`
- `evaluation/results.json`

Metrics:
- Recall@k
- citation hit rate
- simple faithfulness proxy
- average latency
- estimated token cost

These are portfolio metrics, not claims about production performance.

## 7. Feedback loop

`POST /feedback` stores a timestamped user signal in `evaluation/feedback.jsonl`. The project treats feedback as data for later error analysis/retraining rather than pretending that a single feedback event changes the model immediately.

## 8. Tests and CI

```bash
pytest -q
```

GitHub Actions runs the same test suite on pushes and pull requests.

## 9. Data and licensing

The sample corpus contains compact source notes with public source URLs. They are intentionally short and are not a reproduction of the linked documents. Before public deployment, verify each source's current license/terms and refresh the corpus.

## 10. Limitations

- The baseline retriever is lexical TF-IDF rather than a production embedding model.
- Tool calls are local deterministic tools; external enterprise APIs are not connected.
- Faithfulness is measured with a lightweight citation/overlap proxy, not a human benchmark.
- No secret keys are required.

## 11. Job-posting source

Iyuno AI Agent Engineer, Seoul, Hybrid, Full-time, requisition JR101122; the course slide lists the posting deadline as 2026-09-30.
