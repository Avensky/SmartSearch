# 🧠 Semantic PDF Search

This project implements a semantic search system for PDF documents using:

- **Frontend**: React (minimal UI for uploading and querying PDFs)
- **Backend**: Node.js (handles uploads and query proxying)
- **AI Service**: Python FastAPI with `sentence-transformers` and **FAISS + SQLite** for embedding storage and search

---

## 🚀 Features
- Upload and index any number of PDF documents
- Perform semantic searches (e.g., "how to start a fire" matches "lighting a campfire")
- Fast, local-only architecture using **FAISS** for vector search and **SQLite** for metadata

---

## 🧱 Folder Structure
```
semantic-pdf-search/
├── backend/              # Node.js API server
│   ├── server.js
│   └── package.json
│
├── frontend/
│   └── pdf-search-app/   # React frontend (created with Vite or CRA)
│       ├── src/App.js
│       └── package.json
│
├── python_service/       # Python AI microservice
│   ├── search.py
│   ├── requirements.txt
│   └── semantic.index     # FAISS index (binary)
│   └── metadata.db        # SQLite database (PDF info)
```

---

## 🔧 Setup Instructions

### 1. 🧠 Python AI Service
```bash
cd python_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python init_db.py         # (optional) sets up SQLite and FAISS index if not exists
uvicorn search:app --reload --port 8000
```

### 2. 🌐 Node Backend
```bash
cd backend
npm install
node server.js
```

### 3. 💻 React Frontend
```bash
cd frontend/pdf-search-app
npm install
npm run dev
```

---

## 🧪 Example Usage
1. Go to the frontend in browser (usually `http://localhost:5173`)
2. Upload a PDF file
3. Enter a query like `how to start a fire`
4. See semantic matches ranked by relevance

---

## 📦 Dependencies
### Python:
- `fastapi`, `uvicorn`
- `sentence-transformers`
- `pdfminer.six`
- `scikit-learn`, `torch`
- `faiss-cpu` (for vector search)
- `sqlite3` *(built-in with Python stdlib)*

### Node.js:
- `express`, `multer`, `axios`, `cors`

### React:
- `axios`

---

## 📌 Notes
- FAISS handles high-speed similarity search
- SQLite stores chunked text, filenames, and match metadata
- Embeddings are saved in `semantic.index`
- Easily extendable to use persistent vector DBs like Qdrant or Weaviate

---

## 📜 License
MIT

<!-- 

python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
source venv/bin/activate
uvicorn search:app --reload --port 8000
python3 init_db.py 
http://localhost:8000/docs

-->
