import os
import json
import sqlite3
OUTPUT_PATH = "sft_dataset.jsonl"

from config import DB_PATH

def extract_chunks_from_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chunk FROM chunks")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def build_instruction_dataset(chunks):
    dataset = []
    for chunk in chunks:
        dataset.append({
            "instruction": "Answer the question based on the following document.",
            "input": f"Here is an excerpt:\n\"{chunk}\"",
            "output": ""  # Optionally fill in responses manually or later via LLM
        })
    return dataset

if __name__ == "__main__":
    chunks = extract_chunks_from_db(DB_PATH)
    dataset = build_instruction_dataset(chunks)

    with open(OUTPUT_PATH, "w") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ SFT dataset written to {OUTPUT_PATH}")



# import json
# from pathlib import Path

# def chunk_text(text, max_chars=500):
#     paragraphs = text.split('\n')
#     chunks = []
#     chunk = ""
#     for para in paragraphs:
#         if len(chunk) + len(para) < max_chars:
#             chunk += para + " "
#         else:
#             chunks.append(chunk.strip())
#             chunk = para + " "
#     if chunk:
#         chunks.append(chunk.strip())
#     return chunks

# def build_sft_examples(pdf_texts):
#     dataset = []
#     for text in pdf_texts:
#         chunks = chunk_text(text)
#         for chunk in chunks:
#             example = {
#                 "instruction": "Answer based on the following document.",
#                 "input": f"Here is an excerpt:\n\"{chunk}\"",
#                 "output": ""  # can be filled manually or LLM-assisted
#             }
#             dataset.append(example)
#     return dataset

# if __name__ == "__main__":
#     # Example: loading a bunch of plain-text PDFs
#     sources = list(Path("docs/").rglob("*.txt"))  # Assume you've converted PDFs to .txt
#     all_texts = [open(path).read() for path in sources]
    
#     sft_dataset = build_sft_examples(all_texts)

#     with open("sft_dataset.jsonl", "w") as f:
#         for item in sft_dataset:
#             f.write(json.dumps(item) + "\n")
