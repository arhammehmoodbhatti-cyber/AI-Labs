from lab6_search import Retriever

FAQ = [
 {"id":"faq:password", "question":"How do I reset my password?", "answer":"Use the recovery link on the login page.", "source":"it_help.txt"},
 {"id":"faq:submit", "question":"Where do I submit my assignment?", "answer":"Use the assignment upload page in the learning portal.", "source":"assessment.txt"},
 {"id":"faq:late", "question":"Can illness justify a late submission?", "answer":"Request an extension with medical evidence before the deadline.", "source":"handbook.txt"},
 {"id":"faq:printer", "question":"What should I do if the printer makes blank pages?", "answer":"Check ink levels and run the printer cleaning utility.", "source":"printer_guide.txt"},
 {"id":"faq:contractor", "question":"Can contractors work remotely?", "answer":"Only when the signed contract explicitly permits it.", "source":"workplace_policy.txt"}
]

def build_bot(backend="tfidf"):
    records = [dict(row, text=row["question"] + " " + row["answer"]) for row in FAQ]
    return Retriever(records, backend)

def reply(engine, query):
    if not query.strip():
        return "Please enter a question."
    for row in FAQ:
        if query.strip().casefold() == row["question"].casefold():
            return row["answer"] + " [source: " + row["source"] + "]"
    hits = engine.search(query)
    if not hits:
        return "No matching FAQ. Please contact the help desk."
    lines = ["Possible matches; choose or rephrase your question:"]
    for row, score in hits:
        lines.append(row["question"] + f" (similarity {score:.3f})")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["tfidf", "embedding"], default="tfidf")
    args = parser.parse_args()
    engine = build_bot(args.backend)
    print("Exact:", reply(engine, "How do I reset my password?"))
    print("Suggestion:\n" + reply(engine, "password recovery"))
    print("Empty:", reply(engine, ""))
    print("Unsupported:", reply(engine, "volcano geology"))
