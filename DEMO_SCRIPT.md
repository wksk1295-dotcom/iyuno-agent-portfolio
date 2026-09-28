# 2-minute demo script

1. Open README and show the job-requirement mapping.
2. Run `python -m agent.ingest` and show 20 source documents loaded.
3. Run `uvicorn app.main:app --reload` and open `/docs`.
4. POST `/ask` with a security question and show the answer + citations.
5. Ask a calculator expression to show tool calling.
6. Run `python -m evaluation.evaluate` and show `metrics.json`.
7. Show pytest/CI and the feedback endpoint.
