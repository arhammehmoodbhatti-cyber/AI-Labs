import re

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944",
    "",
    "یہ ایک مثال ہے",
    "Version 2.1 is ready."
]

for sample in samples:
    whitespace = sample.split()
    words = re.findall(r"\b\w+\b", sample, flags=re.UNICODE)
    print("Original:", repr(sample))
    print("Whitespace:", whitespace, "count:", len(whitespace))
    print("Word-like:", words, "count:", len(words))
    print()

try:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    for sample in samples[:2]:
        print("Model tokens:", sample, tokenizer.tokenize(sample))
except Exception as error:
    print("Model tokenizer not available:", type(error).__name__)
