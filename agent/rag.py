from pathlib import Path
import json, re, time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "data" / "docs"

def load_documents():
    docs = []
    for p in sorted(DOCS.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        meta = {"id": p.stem, "path": str(p)}
        url = re.search(r"^source_url:\s*(.+)$", text, re.M)
        title = re.search(r"^title:\s*(.+)$", text, re.M)
        meta["source_url"] = url.group(1).strip() if url else ""
        meta["title"] = title.group(1).strip() if title else p.stem
        body = re.sub(r"^(source_url|title):.*\n?", "", text, flags=re.M).strip()
        docs.append({**meta, "text": body})
    return docs

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)] or [""]

class Retriever:
    def __init__(self):
        self.docs = load_documents()
        self.chunks = []
        self.meta = []
        for d in self.docs:
            for idx, c in enumerate(chunk_text(d["text"])):
                self.chunks.append(c)
                self.meta.append({**d, "chunk_id": idx})
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def search(self, query, k=3):
        started = time.perf_counter()
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        order = scores.argsort()[::-1][:k]
        latency_ms = (time.perf_counter() - started) * 1000
        out = []
        for i in order:
            m = self.meta[i].copy()
            m["score"] = float(scores[i])
            m["text"] = self.chunks[i]
            out.append(m)
        return out, latency_ms

def build_answer(question, results):
    if not results or results[0]["score"] <= 0:
        return "관련 근거를 찾지 못했습니다. 질문을 더 구체화해 주세요.", []
    snippets = []
    citations = []
    for r in results[:2]:
        snippets.append(r["text"])
        citations.append({"id": r["id"], "title": r["title"], "url": r["source_url"]})
    answer = "근거 기반 요약:\n" + "\n".join(f"- {s}" for s in snippets)
    return answer, citations
