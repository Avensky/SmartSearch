from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
import os

from config import FAISS_PATH, DB_PATH, EMBEDDING_DIM

# Create a new FAISS index
index = faiss.read_index(FAISS_PATH)
faiss.write_index(index, FAISS_PATH)
print(f"✅ FAISS index initialized and saved to '{FAISS_PATH}'")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Create or reset SQLite DB
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    filehash TEXT,
    chunk TEXT
)''')
c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_filehash_chunk ON chunks(filehash, chunk)')
conn.commit()
conn.close()
print(f"✅ SQLite database initialized and saved to '{DB_PATH}'")

import hashlib
from pdfminer.high_level import extract_text

def split_into_chunks(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def add_files_to_index(file_paths):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(FAISS_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for path in file_paths:
        if not os.path.exists(path):
            print(f"⚠️ Skipping missing file: {path}")
            continue

        try:
            text = extract_text(path)
            chunks = split_into_chunks(text)
            print(f"📄 '{path}' -> {len(chunks)} chunks")

            for chunk in chunks:
                filehash = hashlib.md5((path + chunk).encode()).hexdigest()
                embedding = model.encode(chunk).astype('float32')
                index.add(embedding.reshape(1, -1))
                c.execute("INSERT OR IGNORE INTO chunks (filename, filehash, chunk) VALUES (?, ?, ?)",
                          (path, filehash, chunk))

        except Exception as e:
            print(f"❌ Failed to process '{path}': {e}")

    faiss.write_index(index, FAISS_PATH)
    conn.commit()
    conn.close()
    print("✅ All files processed and saved to index/database.")