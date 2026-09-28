from agent.rag import Retriever
def test_retriever_returns_results():
    r = Retriever()
    results, latency = r.search("What is FastAPI?", k=3)
    assert results
    assert results[0]["id"]
    assert latency >= 0
