import ast, operator as op, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "policies.json"

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow}

def calculator(expression: str):
    tree = ast.parse(expression, mode="eval")
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
        raise ValueError("Only safe arithmetic is allowed.")
    return {"tool": "calculator", "result": ev(tree)}

def policy_lookup(key: str):
    data = json.loads(POLICY.read_text(encoding="utf-8"))
    return {"tool": "policy_lookup", "key": key, "result": data.get(key, "No matching policy.")}

def source_search(query: str):
    from .rag import load_documents
    q = query.lower()
    hits = []
    for d in load_documents():
        if q in (d["title"] + " " + d["text"]).lower():
            hits.append({"id": d["id"], "title": d["title"], "url": d["source_url"]})
    return {"tool": "source_search", "query": query, "results": hits[:5]}
