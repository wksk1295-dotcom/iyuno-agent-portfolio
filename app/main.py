from fastapi import FastAPI
from pydantic import BaseModel, Field
from agent.router import Agent
from agent.feedback import save_feedback

app = FastAPI(title="Iyuno Agent Portfolio", version="1.0.0")
agent = Agent()

class AskRequest(BaseModel):
    question: str = Field(min_length=2)

class FeedbackRequest(BaseModel):
    question: str
    rating: int = Field(ge=1, le=5)
    comment: str = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    return agent.run(req.question)

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    return save_feedback(req.question, req.rating, req.comment)
