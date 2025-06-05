import os
import sqlite3
from utils import compute_file_hash
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

EMBEDDING_DIM = 384
FAISS_PATH = "semantic.index"
DB_PATH = "metadata.db"
PDF_DIR = "docs"

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(FAISS_PATH)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def insert_pdf(file_path):
    filehash = compute_file_hash(file_path)
    cursor.execute("SELECT 1 FROM chunks WHERE filehash = ?", (filehash,))
    if cursor.fetchone():
        print(f"⏩ Skipping (duplicate): {file_path}")
        return

    print(f"📄 Processing: {file_path}")
    text = extract_text(file_path)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    vectors = model.encode(chunks)

    for chunk, vec in zip(chunks, vectors):
        cursor.execute("INSERT INTO chunks (filename, filehash, chunk) VALUES (?, ?, ?)", (os.path.basename(file_path), filehash, chunk))
        index.add(np.array([vec]).astype("float32"))

    conn.commit()
    print(f"✅ Indexed: {file_path}")

for root, _, files in os.walk(PDF_DIR):
    for file in files:
        if file.lower().endswith(".pdf"):
            insert_pdf(os.path.join(root, file))

faiss.write_index(index, FAISS_PATH)
conn.close()
print("🎉 All PDFs processed.")
