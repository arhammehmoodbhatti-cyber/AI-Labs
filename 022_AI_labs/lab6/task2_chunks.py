import json
import re
from pathlib import Path

def word_spans(text):
    return [(match.start(), match.end()) for match in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    result = []
    step = size - overlap
    for start in range(0, len(spans), step):
        end_index = min(start + size, len(spans))
        result.append((offset + spans[start][0], offset + spans[end_index - 1][1]))
        if end_index == len(spans):
            break
    return result

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    cuts = [0] + [match.end() for match in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    output = []
    pending = None
    count = 0
    for start, end in zip(cuts, cuts[1:]):
        segment = text[start:end]
        amount = len(segment.split())
        if amount == 0:
            continue
        if amount > size:
            if pending is not None:
                output.append(pending)
                pending = None
                count = 0
            output.extend(windows(segment, size, 0, start))
        elif pending is not None and count + amount <= size:
            pending = (pending[0], end)
            count += amount
        else:
            if pending is not None:
                output.append(pending)
            pending = (start, end)
            count = amount
    if pending is not None:
        output.append(pending)
    return output

def make_chunks(documents, strategy):
    output = []
    for doc_id, text in documents.items():
        if strategy == "sentence":
            spans = sentence_chunks(text, 40)
        else:
            spans = windows(text, 40, int(strategy))
        for index, (start, end) in enumerate(spans):
            output.append({"id": f"{doc_id}:{index}", "doc": doc_id,
                           "start": start, "end": end,
                           "text": text[start:end]})
    return output

if __name__ == "__main__":
    documents = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(documents, strategy)
        sizes = [len(chunk["text"].split()) for chunk in chunks]
        original_words = sum(len(value.split()) for value in documents.values())
        emitted_words = sum(sizes)
        covered = any("medical evidence is submitted before the deadline" in chunk["text"]
                      for chunk in chunks if chunk["doc"] == "late_rule")
        print("\nStrategy:", strategy, "chunks:", len(chunks),
              "min/max words:", min(sizes), max(sizes),
              "repeated word units:", emitted_words - original_words,
              "rule and exception together:", covered)
        for chunk in chunks[:3]:
            assert documents[chunk["doc"]][chunk["start"]:chunk["end"]] == chunk["text"]
            print(chunk["id"], chunk["start"], chunk["end"], len(chunk["text"].split()))
    assert windows("") == []
    assert len(windows("short text")) == 1
    try:
        windows("a b", 2, 2)
    except ValueError:
        print("Invalid overlap check passed")
    else:
        raise AssertionError("Invalid overlap was accepted")
    long_sentence = " ".join(["word"] * 95) + "."
    assert all(len(long_sentence[a:b].split()) <= 40 for a, b in sentence_chunks(long_sentence))
    print("Long sentence fallback check passed")
