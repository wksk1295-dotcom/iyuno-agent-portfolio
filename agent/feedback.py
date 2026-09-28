from pathlib import Path
import json, datetime
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "feedback.jsonl"

def save_feedback(question, rating, comment=""):
    OUT.parent.mkdir(exist_ok=True)
    row = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "question": question, "rating": rating, "comment": comment}
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
