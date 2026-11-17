import json
from pathlib import Path
from task2_chunks import make_chunks
from lab6_search import Retriever

if __name__ == "__main__":
    documents = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
    engine = Retriever(make_chunks(documents, "0"), "tfidf")
    print("Evidence assistant. Type exit to stop.")
    while True:
        try:
            query = input("Question: ")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() == "exit":
            break
        hits = engine.search(query)
        if not hits:
            print("No candidate evidence. Rephrase or contact a human.")
            continue
        print("Candidate evidence; check the source before using it:")
        for number, (record, score) in enumerate(hits, 1):
            print(number, record["id"], f"{score:.3f}",
                  "characters", record["start"], record["end"])
        chosen = input("Choose 1-3 to inspect; Enter if none apply: ")
        if not chosen.isdigit() or not 1 <= int(chosen) <= len(hits):
            print("No answer selected. Rephrase or contact a human.")
            continue
        record, score = hits[int(chosen) - 1]
        print("Retrieved passage:", record["text"])
        print("Source:", record["doc"], "characters", record["start"], record["end"])
