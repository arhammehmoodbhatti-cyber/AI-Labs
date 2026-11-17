from lab6_search import Retriever, show_hits

records = [
 {"id":"returns:damage", "source":"returns.txt", "region":"PK", "text":"For a damaged parcel, contact support within 48 hours and attach photographs of the item and packaging."},
 {"id":"returns:change", "source":"returns.txt", "region":"PK", "text":"For a change of mind, return unused items within 14 days."},
 {"id":"returns:other", "source":"returns.txt", "region":"OTHER", "text":"Damaged parcel reports in another region have a 72 hour window."}
]
engine = Retriever(records)
show_hits(engine.search("broken parcel photographs", k=2, filters={"region": "PK"}))
