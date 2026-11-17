import json
from pathlib import Path
from task2_chunks import make_chunks
from lab6_search import Retriever

documents = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
chunks = make_chunks(documents, "sentence")
queries = [
    "How can I regain access to my account?",
    "Where can I hand in my coursework?",
    "What should I do when my printer produces empty sheets?"
]
for backend in ["tfidf", "embedding"]:
    try:
        engine = Retriever(chunks, backend)
        print("Backend:", backend)
        for query in queries:
            print("Query:", query)
            for record, score in engine.search(query, k=2):
                print(record["id"], f"{score:.3f}", record["doc"],
                      record["start"], record["end"], record["text"])
    except Exception as error:
        print("Backend not run:", backend, type(error).__name__, str(error))
