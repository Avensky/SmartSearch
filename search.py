from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from pdfminer.high_level import extract_text
import faiss
import sqlite3
import tempfile
import os
import numpy as np

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Model and FAISS config
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_dim = 384
faiss_path = "semantic.index"
db_path = "metadata.db"

# Load or create FAISS index
if os.path.exists(faiss_path):
    index = faiss.read_index(faiss_path)
else:
    index = faiss.IndexFlatL2(embedding_dim)

# SQLite connection and table
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    chunk TEXT
)''')
conn.commit()

# Helper to chunk text
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(' '.join(words[i:i + chunk_size]))
    return chunks

@app.post("/upload")
async def upload(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        text = extract_text(tmp.name)

    chunks = chunk_text(text)
    embeddings = model.encode(chunks, convert_to_numpy=True).astype('float32')
    index.add(np.array(embeddings))

    c.executemany("INSERT INTO chunks (filename, chunk) VALUES (?, ?)", [(file.filename, chunk) for chunk in chunks])
    conn.commit()
    faiss.write_index(index, faiss_path)

    return {"message": f"{file.filename} uploaded and embedded", "chunks": len(chunks)}

@app.get("/search")
def search(query: str):
    query_vec = model.encode([query], convert_to_numpy=True).astype('float32')
    D, I = index.search(query_vec, 5)
    c.execute("SELECT filename, chunk FROM chunks")
    all_chunks = c.fetchall()

    results = []
    for rank, idx in enumerate(I[0]):
        if idx < len(all_chunks):
            filename, snippet = all_chunks[idx]
            results.append({
                "filename": filename,
                "snippet": snippet,
                "score": float(D[0][rank])
            })
    return results
