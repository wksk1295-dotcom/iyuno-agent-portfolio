from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health():
    assert client.get("/health").json()["status"] == "ok"
def test_ask():
    r = client.post("/ask", json={"question":"What does FastAPI provide?"})
    assert r.status_code == 200
    assert "citations" in r.json()
