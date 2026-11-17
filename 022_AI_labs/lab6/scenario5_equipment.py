from lab6_search import Retriever, show_hits

records = [
 {"id":"printer:blank", "source":"manual.txt", "device":"printer", "text":"For blank printer pages: check ink level, run the printer cleaning utility, and print a test page."},
 {"id":"scanner:blank", "source":"scanner.txt", "device":"scanner", "text":"For a blank scanner image, check document placement and select the correct scanning source."}
]
engine = Retriever(records)
show_hits(engine.search("blank pages", k=2, filters={"device": "printer"}))
