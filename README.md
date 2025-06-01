# AI Interview Preparation Chatbot

An intelligent chatbot powered by LangChain and RAG (Retrieval-Augmented Generation) to help users prepare for technical interviews across various roles.

## Core Features

### 1. Role-Based Interview Preparation
- Choose from multiple engineering roles:
  - Frontend Engineer
  - Backend Engineer
  - Full-stack Engineer
  - Data Scientist / Analyst
  - DevOps Engineer
  - AI/ML Engineer
  - QA/Testing Engineer

### 2. RAG-Powered Q&A Engine
- Utilizes LangChain and FAISS for intelligent answer retrieval
- Sources answers from:
  - Technical interview guides
  - Job descriptions
  - Coding platforms content
  - Role-specific documentation

### 3. Question Type Support
- Technical Theory Questions
- Coding Problems
- Behavioral Questions
- System Design Challenges
- Resume-Based Questions

### 4. Progress Tracking
- Topic-wise progress monitoring
- Study streak tracking
- Personalized topic recommendations
- Visual progress indicators

### 5. Interactive Features
- Real-time feedback collection
- Answer quality ratings
- Helpful/Not helpful indicators
- Comment submission

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- LangChain
- FAISS Vector Store
- PostgreSQL

### Frontend
- React
- TypeScript
- Material-UI
- React Query

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-interview-chatbot
```

2. Set up the Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Install frontend dependencies:
```bash
cd frontend
npm install
```

6. Start the development servers:

Backend:
```bash
uvicorn src.main:app --reload
```

Frontend:
```bash
npm run dev
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

## Project Structure

```
.
├── src/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── services/
│       ├── rag_service.py
│       └── progress_service.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RoleSelector.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   └── FeedbackDialog.tsx
│   │   └── App.tsx
│   └── package.json
├── data/
│   ├── frontend/
│   ├── backend/
│   ├── fullstack/
│   ├── data_science/
│   ├── devops/
│   ├── ai_ml/
│   └── qa/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 