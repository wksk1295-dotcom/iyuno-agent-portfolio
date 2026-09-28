from .rag import load_documents, chunk_text
def main():
    docs = load_documents()
    chunks = sum(len(chunk_text(d["text"])) for d in docs)
    print(f"Loaded {len(docs)} source documents / {chunks} chunks.")
if __name__ == "__main__":
    main()
