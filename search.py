from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from pdfminer.high_level import extract_text
from llm import ask_llm
import faiss
import sqlite3
import tempfile
import os
import numpy as np
from config import FAISS_PATH, DB_PATH, EMBEDDING_DIM
from utils import compute_file_hash
from pydantic import BaseModel


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Model and FAISS config
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Load or create FAISS index
if os.path.exists(FAISS_PATH):
    index = faiss.read_index(FAISS_PATH)
else:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)

# SQLite connection and table
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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



class UploadDirRequest(BaseModel):
    path: str

@app.post("/upload_dir")
def upload_directory(data: UploadDirRequest):
    directory = data.path
    if not os.path.isdir(directory):
        raise HTTPException(status_code=400, detail=f"Invalid directory: {directory}")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(FAISS_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    added_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(root, file)
            filehash = compute_file_hash(file_path)

            # Skip if file already exists
            cursor.execute("SELECT 1 FROM chunks WHERE filehash = ?", (filehash,))
            if cursor.fetchone():
                continue

            try:
                text = extract_text(file_path)
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                embeddings = model.encode(chunks)

                for chunk, vec in zip(chunks, embeddings):
                    cursor.execute("INSERT INTO chunks (filename, filehash, chunk) VALUES (?, ?, ?)",
                                   (os.path.basename(file_path), filehash, chunk))
                    index.add(np.array([vec]).astype("float32"))

                added_files += 1
                print(f"✅ Indexed: {file_path}")

            except Exception as e:
                print(f"❌ Failed to process {file_path}: {e}")

    conn.commit()
    faiss.write_index(index, FAISS_PATH)
    conn.close()

    return { "status": "done", "indexed_files": added_files }



@app.post("/upload")
async def upload(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        text = extract_text(tmp.name)

    chunks = chunk_text(text)
    embeddings = MODEL.encode(chunks, convert_to_numpy=True).astype('float32')
    index.add(np.array(embeddings))

    c.executemany("INSERT INTO chunks (filename, chunk) VALUES (?, ?)", [(file.filename, chunk) for chunk in chunks])
    conn.commit()
    faiss.write_index(index, FAISS_PATH)

    return {"message": f"{file.filename} uploaded and embedded", "chunks": len(chunks)}
from fastapi.responses import JSONResponse

@app.get("/search")
def search(query: str):
    # Load index and metadata
    index = faiss.read_index(FAISS_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Encode query
    query_vector = MODEL.encode([query])
    D, I = index.search(query_vector, k=5)

    # Retrieve text chunks by index
    c.execute("SELECT chunk FROM chunks")
    rows = c.fetchall()
    texts = [r[0] for r in rows]

    top_chunks = []
    for i, score in zip(I[0], D[0]):
        if 0 <= i < len(texts):
            c.execute("SELECT filename FROM chunks WHERE id = ?", (i + 1,))
            filename_row = c.fetchone()
            top_chunks.append({
                "filename": filename_row[0] if filename_row else "unknown",
                "snippet": texts[i][:300],
                "score": float(score)
            })

    # Decide: LLM or chunks
    if len(top_chunks) > 0 and float(D[0][0]) < 1.5:  # Threshold for relevance
        return JSONResponse(content={
            "type": "chunks",
            "results": top_chunks,
            "answer": None
        })
    else:
        # LLM fallback
        context = "\n".join([t["snippet"] for t in top_chunks])
        answer = ask_llm(context, query)

        return JSONResponse(content={
            "type": "llm",
            "results": [],
            "answer": answer
        })