import faiss
import sqlite3
import os

FAISS_PATH = "semantic.index"
DB_PATH = "metadata.db"
EMBEDDING_DIM = 384

# Create or reset FAISS index
index = faiss.IndexFlatL2(EMBEDDING_DIM)
faiss.write_index(index, FAISS_PATH)
print(f"✅ FAISS index initialized and saved to '{FAISS_PATH}'")

# Create or reset SQLite DB
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    chunk TEXT
)''')
conn.commit()
conn.close()
print(f"✅ SQLite database initialized and saved to '{DB_PATH}'")
