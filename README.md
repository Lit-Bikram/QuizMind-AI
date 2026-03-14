# QuizMind AI 🧠📘

**QuizMind AI** is a full-stack AI-powered application that generates **high-quality multiple-choice questions (MCQs)** from uploaded PDF documents using **LLMs, focused retrieval, and verification logic**.

Users can upload a PDF, provide a query/topic, choose the number of questions, take the quiz in a clean React interface, and receive a detailed performance dashboard with score, difficulty breakdown, question review, and weak areas.

---

## 🚀 Features

- 📄 Upload PDF documents for content extraction
- 🎯 Query-focused MCQ generation from relevant document context
- 🤖 LLM-powered question generation
- ✅ Question verification / filtering for better quality
- 📝 Interactive quiz interface with one-question-at-a-time flow
- 📊 Results dashboard with:
  - Score percentage
  - Correct / incorrect count
  - Difficulty breakdown
  - Question review
  - Weak areas analysis
- ⚡ Full-stack integration with FastAPI backend + React TypeScript frontend

---

## 🧠 How It Works

1. User uploads a **PDF**
2. User enters a **query/topic**
3. Backend:
   - Parses PDF text
   - Splits content into chunks
   - Extracts keyphrases
   - Retrieves focused context relevant to the query
   - Uses an LLM to generate MCQs
   - Filters / verifies questions for quality
4. Frontend displays the quiz
5. User submits answers
6. Backend scores the quiz and returns analytics
7. Frontend renders a results dashboard

> **Note:** The app may return fewer questions than requested if the document-query pair does not support enough high-confidence MCQs. This is intentional to prioritize quality over hallucinated output.

---

## 🛠️ Tech Stack

### Frontend
- **React**
- **TypeScript**
- **Vite**
- **React Router DOM**
- **Axios**
- **React Toastify**
- **Lucide React**

### Backend
- **FastAPI**
- **Python**
- **Pydantic**
- **python-dotenv**
- **Uvicorn**

### AI / NLP / Retrieval
- **LLM API (Groq / OpenAI compatible)**
- **Query-focused context extraction**
- **Chunking + keyphrase-based retrieval**
- **Verification-aware MCQ generation**

---

## 📁 Project Structure

```bash
QuizMind-AI/
│
├── backend/
│   ├── app/
│   ├── uploaded_docs/
│   ├── .env.example
│   ├── requirements.txt
│   └── ...
│
├── ai-mcq-frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── upload/
│   │   │   ├── quiz/
│   │   │   └── results/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
