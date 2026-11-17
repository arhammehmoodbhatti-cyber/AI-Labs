from lab6_search import Retriever, show_hits

records = [{'id': 'course:upload', 'source': 'course.txt', 'text': 'Upload assignments through the learning portal. Submit the final file as a PDF and keep the receipt.'}, {'id': 'course:late', 'source': 'course.txt', 'text': 'Late submissions are normally penalized unless an approved exception applies.'}]
engine = Retriever(records)
show_hits(engine.search('where do I hand in coursework', k=2))
