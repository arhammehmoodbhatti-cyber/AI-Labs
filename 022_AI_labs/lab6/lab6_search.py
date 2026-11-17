import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Retriever:
    def __init__(self, records, backend="tfidf", model=None):
        if not records or any(not row["text"].strip() for row in records):
            raise ValueError("Provide nonempty records")
        self.records = records
        self.backend = backend
        self.model = model
        texts = [row["text"] for row in records]
        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(texts)
        elif backend == "embedding":
            if self.model is None:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
            self.check_length(texts)
            self.matrix = self.model.encode(texts, normalize_embeddings=True)
        else:
            raise ValueError("Use tfidf or embedding")

    def check_length(self, texts):
        for item in texts:
            count = len(self.model.tokenizer(item, truncation=False)["input_ids"])
            if count > self.model.max_seq_length:
                raise ValueError("Input exceeds encoder token limit")

    def search(self, query, k=3, filters=None):
        if not query.strip() or k <= 0:
            return []
        if self.backend == "tfidf":
            vector = self.vectorizer.transform([query])
            if vector.nnz == 0:
                return []
            scores = (vector @ self.matrix.T).toarray()[0]
        else:
            self.check_length([query])
            vector = self.model.encode([query], normalize_embeddings=True)[0]
            scores = self.matrix @ vector
        allowed = [i for i, row in enumerate(self.records)
                   if all(row.get(key) == value for key, value in (filters or {}).items())]
        ranked = sorted(allowed, key=lambda i: (-float(scores[i]), i))
        return [(self.records[i], float(scores[i])) for i in ranked[:k]]

def show_hits(hits):
    if not hits:
        print("No matching records.")
    for record, score in hits:
        print(record["id"], f"score={score:.3f}", record["text"])
