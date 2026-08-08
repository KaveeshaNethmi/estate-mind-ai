# 🏡 EstateMind AI — Real Estate AI Copilot

EstateMind AI is a production-style **Retrieval-Augmented Generation (RAG)** application for conversational real estate search and investment analysis.

Users can ask natural-language questions about Dubai properties, compare listings, apply structured filters, explore market insights, and receive answers grounded in retrieved property data.

The project now includes:

- A **FastAPI backend** with Manual RAG, LangChain RAG, and Pinecone implementations
- A **React + TypeScript frontend** with a responsive dashboard interface
- Conversational memory, query rewriting, metadata filtering, reranking, citations, confidence scoring, and streaming responses

---

### 🎯 Project Goals

EstateMind AI was created to understand how production-style RAG systems evolve from first principles into scalable AI applications.

The project compares three retrieval approaches:

1. **Manual RAG**
   - Built using OpenAI embeddings, FAISS, NumPy, and FastAPI
   - Provides full control over indexing, retrieval, filtering, and context construction

2. **LangChain RAG**
   - Uses LangChain abstractions for documents, embeddings, retrieval, prompts, and LLM orchestration

3. **Pinecone RAG**
   - Uses a managed cloud vector database for persistent and scalable semantic search

The frontend is being developed as a premium AI real estate copilot for Dubai property discovery and investment analysis.

---

### ✨ Current Product Experience

The current frontend foundation includes:

- Responsive dashboard layout
- Collapsible left navigation
- Independent main-content and right-panel scrolling
- EstateMind AI assistant modes
  - Market Insights
  - Investment Analysis
- Suggested conversational prompts
- AI property-search input
- Dubai Market Pulse panel
- Search results route
- Property details route
- Reusable design-system tokens using Tailwind CSS v4

The search-results and property-details screens are currently being implemented.

---

# 🏗 System Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                         React Frontend                        │
│  Natural-language search • Market insights • Property UI      │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                       │
│ Chat API • Conversation state • Filters • Streaming           │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
                    Query Rewriting & Filtering
                               │
                               ▼
                       Query Embedding
                               │
                               ▼
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
       Manual FAISS      LangChain FAISS       Pinecone
            │                  │                  │
            └──────────────────┴──────────────────┘
                               │
                               ▼
                   Retrieval and Reranking
                               │
                               ▼
                    Context Construction
                               │
                               ▼
                      OpenAI GPT Model
                               │
                               ▼
          Grounded Answer • Sources • Confidence Score
```

---


| Implementation | Vector Store | Embeddings       | Retrieval           | Purpose                                               |
|----------------|--------------|------------------|---------------------|-------------------------------------------------------|
| Manual RAG     | FAISS        | OpenAI           | Custom Python       | Learn the complete RAG pipeline from first principles |
| LangChain RAG  | FAISS        | OpenAIEmbeddings | LangChain Retriever | Learn framework-based AI development                  |
| Pinecone RAG   | Pinecone     | OpenAI           | Pinecone Query API  | Learn production-ready cloud vector search            |


---

### 🔄 End-to-End Workflow

```text
MongoDB Property Documents
            │
            ▼
    Property Formatter
  (JSON → Semantic Text)
            │
            ▼
      OpenAI Embeddings
  (text-embedding-3-small)
            │
            ▼
Manual FAISS / LangChain FAISS / Pinecone
            │
            ▼
Semantic Similarity Search
            │
            ▼
    Metadata Filtering
            │
            ▼
        Reranking
            │
            ▼
    Context Construction
            │
            ▼
     OpenAI GPT Model
            │
            ▼
Streaming Grounded Response
```

---

# 🚀 Features

### 🤖 AI and RAG

- Retrieval-Augmented Generation
- Context-grounded LLM responses
- OpenAI embedding generation
- Semantic similarity search
- Hybrid semantic and metadata retrieval
- Query rewriting
- Natural-language filter extraction
- Reranking
- Source citations
- Confidence scores
- Streaming responses

### 💬 Conversational Intelligence

- Multi-turn conversations
- Conversation history
- Search-state persistence
- Follow-up question understanding
- Entity-aware property references
- Context-aware property selection
- Property comparison

Example conversation:

```text
Show me apartments in Meydan.

Compare the first two.

Which one is cheaper?

What is the ROI of the second one?

Now show me villas instead.
```

### 🔎 Structured Filters

Supported filters include:

- City
- Area
- Development
- Property type
- Maximum price
- Minimum bedrooms

### 🏠 Real Estate Copilot

Users can ask questions such as:

- Show me furnished apartments in Meydan with good rental yield.
- Which areas currently offer the strongest investment potential?
- Compare Dubai Marina and Downtown Dubai.
- Show apartments below AED 2 million.
- Which property has the better ROI?
- Find family-friendly communities near schools.
- Recommend luxury villas in Palm Jumeirah.
- Show similar properties to the second result.

### 🖥 Frontend

- React + TypeScript
- Responsive dashboard layout
- Tailwind CSS v4 design tokens
- Reusable page shell
- Left navigation
- Assistant-mode tabs
- Suggested prompt cards
- Dubai Market Pulse panel
- Property search input
- Search and property-detail routes

### ⚙️ Backend

- FastAPI REST API
- Swagger/OpenAPI documentation
- MongoDB integration
- Environment-based configuration
- Modular service-oriented architecture
- Separate Manual RAG, LangChain, and Pinecone implementations
- Async request handling
- Streaming responses

---

# 🛠 Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS v4
- React Router
- Lucide React

### Backend

- Python
- FastAPI
- Pydantic
- PyMongo
- python-dotenv

### AI and LLM

- OpenAI GPT
- OpenAI `text-embedding-3-small`
- LangChain

### Vector Search

- FAISS
- LangChain FAISS VectorStore
- Pinecone

### Database

- MongoDB

---

# 📂 Project Structure

```text
estate-mind-ai/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── router.tsx
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   ├── layout/
│   │   │   ├── market/
│   │   │   └── property/
│   │   ├── data/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── styles/
│   │   │   └── global.css
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── chat_routes.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── schemas/
│   │   │   ├── chat_schema.py
│   │   │   ├── entity_reference_schema.py
│   │   │   ├── filter_schema.py
│   │   │   └── reranking_schema.py
│   │   ├── services/
│   │   │   ├── manual_rag/
│   │   │   ├── langchain_rag/
│   │   │   ├── pinecone_rag/
│   │   │   ├── citation_service.py
│   │   │   ├── confidence_service.py
│   │   │   ├── entity_reference_service.py
│   │   │   ├── filter_extraction_service.py
│   │   │   ├── property_formatter.py
│   │   │   ├── reranking_service.py
│   │   │   ├── search_state_service.py
│   │   │   └── streaming_service.py
│   │   └── main.py
│   ├── scripts/
│   │   ├── build_manual_faiss_index.py
│   │   ├── build_langchain_faiss_index.py
│   │   ├── build_pinecone_index.py
│   │   ├── test_manual_retrieval.py
│   │   ├── test_langchain_retrieval.py
│   │   ├── test_filter_extraction.py
│   │   └── test_entity_reference.py
│   ├── vector_store/
│   │   └── .gitkeep
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

# ⚙️ How It Works

### 1. Property Formatting

Each MongoDB property document is converted into semantic text.

Example:

```text
1-bedroom furnished apartment located in Meydan, Dubai.

Price: 1,050,700 AED
Rental Yield: 5.1%
ROI 15 Years: 75.4%

Amenities:
Shared Spa
Restaurants
Public Parking
Children's Play Area
```

This improves retrieval quality because embedding models understand semantic text more effectively than raw JSON.

### 2. Embedding Generation

The formatted property text is converted into embeddings using:

```text
text-embedding-3-small
```

Each property becomes a numerical vector representing its semantic meaning.

### 3. Vector Indexing

Manual FAISS:

```text
backend/vector_store/
├── properties.index
└── metadata.json
```

LangChain FAISS:

```text
backend/vector_store/langchain_faiss_index/
├── index.faiss
└── index.pkl
```

Pinecone stores vectors in a managed cloud index.

Generated vector files are excluded from Git and can be rebuilt using the indexing scripts.

### 4. Retrieval

For every question, the backend:

1. Rewrites the query when required
2. Extracts structured filters
3. Generates a query embedding
4. Performs semantic search
5. Applies metadata filters
6. Reranks retrieved properties
7. Builds context for the LLM

### 5. Response Generation

The LLM answers using retrieved property context rather than relying only on pre-trained knowledge.

Responses can include:

- Grounded property recommendations
- Comparisons
- Source citations
- Confidence scores
- Streaming output

---

# 📌 API Endpoints

### Manual RAG

```http
POST /chat/manual
```

### LangChain RAG

```http
POST /chat/langchain
```

### Pinecone RAG

```http
POST /chat/pinecone
```

Example request:

```json
{
  "question": "Show me furnished apartments in Meydan with good rental yield.",
  "top_k": 5,
  "development": "Meydan",
  "property_type": "Apartment",
  "max_price": 1200000
}
```

Example response:

```json
{
  "answer": "...",
  "sources": [],
  "confidence": 0.89
}
```

---

# ▶️ Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/KaveeshaNethmi/estate-mind-ai.git
cd estate-mind-ai
```

### 2. Run the backend

```bash
cd backend
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://localhost:27017
DB_NAME=your_database_name
COLLECTION_NAME=your_collection_name

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=estate-mind-ai
```

Build the required indexes:

```bash
python scripts/build_manual_faiss_index.py
python scripts/build_langchain_faiss_index.py
python scripts/build_pinecone_index.py
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

### 3. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will display the local frontend URL in the terminal.

### 4. Create a production frontend build

```bash
cd frontend
npm run build
```

---

# 🧪 Why Three RAG Implementations?

### Manual RAG

The manual implementation provides full control over:

- Embedding generation
- Vector creation
- FAISS indexing
- Metadata mapping
- Similarity search
- Context construction
- Prompt engineering
- Response generation

It demonstrates how RAG works without framework abstractions.

### LangChain RAG

LangChain simplifies:

- Document management
- Embedding generation
- Vector-store integration
- Retrieval
- Prompt templating
- LLM orchestration

It demonstrates how AI frameworks accelerate development.

### Pinecone RAG

Pinecone provides:

- Cloud-hosted vector storage
- Persistent vector indexes
- Metadata filtering
- Scalable semantic search
- Multi-instance access

It demonstrates how a local RAG pipeline can evolve into a cloud-oriented architecture.

---

# 📖 Key Learnings

### AI Engineering

- Retrieval-Augmented Generation
- OpenAI embeddings
- Semantic search
- Prompt engineering
- Context grounding
- Hybrid retrieval
- Metadata filtering
- Conversational state
- Reranking
- Source citation
- Confidence scoring
- Streaming responses

### Vector Databases

- FAISS
- Pinecone
- Similarity search
- Nearest-neighbour retrieval
- Vector indexing
- Cloud vector databases

### Frontend Engineering

- React and TypeScript
- Vite
- Tailwind CSS v4
- Responsive dashboard architecture
- Reusable component design
- Route-based page composition
- Design-system tokens

### Backend Engineering

- FastAPI
- REST API development
- MongoDB integration
- Async request handling
- Modular architecture
- Service-oriented backend design

---

# 🗺 Roadmap

### Phase 1 — RAG Foundations ✅

- Manual RAG
- LangChain RAG
- Pinecone integration
- Hybrid retrieval
- Metadata filtering
- FastAPI REST API

### Phase 2 — Conversational Intelligence ✅

- Conversation memory
- Conversation history
- Search-state persistence
- Query rewriting
- Follow-up understanding
- Entity-aware property tracking

### Phase 3 — Retrieval Quality ✅

- Reranking
- Source citations
- Confidence scores
- Streaming responses
- Initial async processing

### Phase 4 — Frontend Foundation 🚧

- Responsive dashboard shell ✅
- Design-system tokens ✅
- Left navigation ✅
- Assistant mode tabs ✅
- Suggested prompts ✅
- Dubai Market Pulse panel ✅
- Search-results page 🚧
- Property-details page 🚧
- Mobile navigation 🚧

### Phase 5 — Production Readiness

- Authentication and authorization
- Background indexing jobs
- Incremental data ingestion
- Docker
- Automated tests
- CI/CD
- Cloud deployment
- Monitoring and logging

### Long-Term Vision

Transform EstateMind AI into a production-ready AI copilot for:

- Conversational property search
- Real estate investment analysis
- Property recommendations
- Portfolio comparison
- Market insights
- Neighbourhood intelligence
- Intelligent real estate decision support

---

# 👩‍💻 Author

**Kaveesha Abeynayake**

Backend-focused Software Engineer transitioning into AI Engineering.

Currently exploring:

- Retrieval-Augmented Generation
- LLM applications
- AI agents
- Vector databases
- Production AI systems
- AI-powered SaaS products
