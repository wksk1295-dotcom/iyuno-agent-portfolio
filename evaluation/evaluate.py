import json, time, statistics
from pathlib import Path
from agent.router import Agent
ROOT = Path(__file__).resolve().parents[1]

def main():
    qs = json.loads((ROOT/"evaluation/questions.json").read_text(encoding="utf-8"))
    agent = Agent()
    results = []
    for item in qs:
        t = time.perf_counter()
        out = agent.run(item["question"])
        ms = (time.perf_counter()-t)*1000
        ids = [x["id"] for x in out["retrieval"]]
        hit = int(item["expected_source"] in ids)
        citation_hit = int(any(c["id"] == item["expected_source"] for c in out["citations"]))
        results.append({"id": item["id"], "expected": item["expected_source"],
                        "retrieved": ids, "hit_at_3": hit,
                        "citation_hit": citation_hit, "latency_ms": round(ms,2)})
    metrics = {
        "questions": len(results),
        "recall_at_3": round(sum(r["hit_at_3"] for r in results)/len(results), 4),
        "citation_hit_rate": round(sum(r["citation_hit"] for r in results)/len(results), 4),
        "avg_latency_ms": round(statistics.mean(r["latency_ms"] for r in results), 2)
    }
    (ROOT/"evaluation/results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT/"evaluation/metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
if __name__ == "__main__":
    main()
