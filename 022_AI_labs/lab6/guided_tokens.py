import re
text = "I can't submit CS4944 late!"
print("Whitespace:", text.split(), len(text.split()))
words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
print("Word-like:", words, len(words))
print("Original:", text)
