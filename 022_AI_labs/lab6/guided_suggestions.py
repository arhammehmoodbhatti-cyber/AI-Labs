from guided_chatbot import build_bot

for backend in ["tfidf", "embedding"]:
    try:
        engine = build_bot(backend)
        print("Backend:", backend)
        for query in ["assignment upload", "forgot login", "can I work from home"]:
            print("Query:", query)
            for record, score in engine.search(query, k=3):
                if backend == "embedding" or score > 0:
                    print(record["id"], record["question"], f"{score:.3f}")
    except Exception as error:
        print("Backend not run:", backend, type(error).__name__, str(error))
