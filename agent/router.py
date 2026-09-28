import re, time
from .rag import Retriever, build_answer
from .tools import calculator, policy_lookup, source_search

class Agent:
    def __init__(self):
        self.retriever = Retriever()

    def run(self, question: str):
        started = time.perf_counter()
        trace = []
        tool_result = None

        calc = re.search(r"(?:calculate|계산)\s*[:=]?\s*([0-9+\-*/(). ]+)$", question, re.I)
        if calc:
            tool_result = calculator(calc.group(1).strip())
            trace.append(tool_result)
        elif any(x in question.lower() for x in ["policy", "정책", "least privilege"]):
            tool_result = policy_lookup("least_privilege")
            trace.append(tool_result)
        elif question.lower().startswith("source:"):
            tool_result = source_search(question.split(":",1)[1].strip())
            trace.append(tool_result)

        results, retrieval_ms = self.retriever.search(question, k=3)
        answer, citations = build_answer(question, results)
        if tool_result:
            answer += f"\n\nTool result: {tool_result['result'] if 'result' in tool_result else tool_result}"

        elapsed = (time.perf_counter() - started) * 1000
        estimated_tokens = max(1, len(question.split()) + sum(len(r["text"].split()) for r in results))
        return {
            "answer": answer,
            "citations": citations,
            "retrieval": [{"id": r["id"], "score": r["score"]} for r in results],
            "trace": trace,
            "metrics": {"latency_ms": round(elapsed, 2), "retrieval_ms": round(retrieval_ms, 2),
                        "estimated_tokens": estimated_tokens,
                        "estimated_cost_usd": round(estimated_tokens * 0.000002, 8)}
        }
