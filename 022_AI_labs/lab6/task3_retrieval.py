import csv
import json
import time
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks


def metrics(rankings, chunks, items):
    hits, reciprocal = [], []
    for row, item in zip(rankings, items):
        if item["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        ranks = [rank for rank, index in enumerate(top, 1)
                 if chunks[index]["doc"] == item["doc"]
                 and item["evidence"] in chunks[index]["text"]]
        hits.append(bool(ranks))
        reciprocal.append(1 / ranks[0] if ranks else 0)
    if not hits:
        return None, None
    return sum(hits) / len(hits), sum(reciprocal) / len(reciprocal)

def main():
    documents = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
    items = json.loads(Path("queries.json").read_text(encoding="utf-8"))
    for item in items:
        assert item["split"] in {"dev", "test"}
        if item["doc"] is not None:
            assert item["evidence"] in documents[item["doc"]]
    logs = []
    model = None
    model_load = None
    try:
        from sentence_transformers import SentenceTransformer
        started = time.perf_counter()
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        model_load = time.perf_counter() - started
        print("Model load seconds:", round(model_load, 3))
    except Exception as error:
        print("Embedding backend unavailable:", type(error).__name__, str(error))
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(documents, strategy)
        texts = [chunk["text"] for chunk in chunks]
        query_texts = [item["query"] for item in items]
        for method in ["tfidf", "embedding"]:
            if method == "embedding" and model is None:
                logs.append({"strategy": strategy, "method": method,
                             "status": "not_run_model_unavailable"})
                continue
            started = time.perf_counter()
            if method == "tfidf":
                vectorizer = TfidfVectorizer()
                C = vectorizer.fit_transform(texts)
                Q = vectorizer.transform(query_texts)
                encode_time = time.perf_counter() - started
                started = time.perf_counter()
                scores = (Q @ C.T).toarray()
            else:
                lengths = [len(model.tokenizer(value, truncation=False)["input_ids"])
                           for value in texts + query_texts]
                if max(lengths) > model.max_seq_length:
                    raise ValueError("Model token limit exceeded")
                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)
                encode_time = time.perf_counter() - started
                started = time.perf_counter()
                scores = Q @ C.T
            search_time = time.perf_counter() - started
            print("\n", strategy, method, "chunks", len(chunks),
                  "encode", round(encode_time, 4), "search", round(search_time, 4))
            for split in ["dev", "test"]:
                indices = [i for i, item in enumerate(items) if item["split"] == split]
                hit, mrr = metrics(scores[indices], chunks, [items[i] for i in indices])
                print(split, "Hit@3", hit, "MRR@3", mrr)
            for row, item in zip(scores, items):
                for rank, index in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                    chunk = chunks[index]
                    record = {"strategy": strategy, "method": method,
                              "query": item["query"], "split": item["split"],
                              "rank": rank, "score": float(row[index]),
                              "chunk_id": chunk["id"], "doc": chunk["doc"],
                              "start": chunk["start"], "end": chunk["end"],
                              "text": chunk["text"],
                              "answerable": item["doc"] is not None,
                              "status": "completed"}
                    logs.append(record)
                    print(rank, chunk["id"], round(float(row[index]), 3),
                          chunk["start"], chunk["end"], chunk["text"][:110])
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as file:
        fields = sorted({key for row in logs for key in row})
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(logs)
    print("Saved retrieval_log.csv")

if __name__ == "__main__":
    main()
