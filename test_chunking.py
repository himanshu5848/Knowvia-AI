
from chunking import chunk_text

text = """
Database normalization reduces data redundancy.
It organizes database tables to improve data integrity.
First Normal Form requires each column to contain atomic values.
"""

chunks = chunk_text(text, chunk_size=60, overlap=10)

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)

print("\nTotal chunks:", len(chunks))