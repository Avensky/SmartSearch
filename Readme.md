# 🧠 Semantic PDF Search

This project implements a semantic search system for PDF documents using:

- **Frontend**: React (minimal UI for uploading and querying PDFs)
- **Backend**: Node.js (handles uploads and query proxying)
- **AI Service**: Python FastAPI with `sentence-transformers` (local embeddings and similarity search)

---

## 🚀 Features
- Upload and index any number of PDF documents
- Perform semantic searches (e.g., "how to start a fire" matches "lighting a campfire")
- Fast, local-only architecture (no external APIs required)

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
│   └── requirements.txt
```

---

## 🔧 Setup Instructions

### 1. 🧠 Python AI Service
```bash
cd python_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn search:app --reload --port 8000
```

### 2. 🌐 Node Backend
```bash
cd backend
npm install
```

### 3. 💻 React Frontend
```bash
cd ../frontend
npm install
cd ..
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

### Node.js:
- `express`, `multer`, `axios`, `cors`

### React:
- `axios`

---

## 📌 Notes
- Embeddings are stored in memory; restart clears uploads/indexes
- Easily extendable to support FAISS, Redis Vector, or DB persistence

---

## 📜 License
MIT
