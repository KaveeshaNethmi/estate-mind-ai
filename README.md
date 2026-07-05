# 🏡 EstateMind AI - Real Estate AI Copilot

A production-style **Retrieval-Augmented Generation (RAG)** application that allows users to interact with a real estate property database using natural language.

EstateMind AI retrieves relevant property data from a vector database, grounds the response with real property information, and generates context-aware answers using an LLM.

## 🎯 Project Goal

The goal of this project is to understand and compare different ways of building a RAG system:

1. **Manual RAG Implementation**  
   Built from first principles using OpenAI Embeddings, FAISS, NumPy, and FastAPI.

2. **LangChain RAG Implementation**  
   Rebuilt using LangChain to understand how AI frameworks simplify RAG development.

3. **Pinecone RAG Implementation**  
   Integrated Pinecone as a managed cloud vector database for a more production-style setup.

This project was built step by step to understand both:

- How RAG works under the hood
- How modern AI frameworks and vector databases improve developer productivity and scalability

---

# 🏗 System Architecture

EstateMind AI follows a Retrieval-Augmented Generation (RAG) architecture where the Large Language Model answers questions using retrieved property data instead of relying only on its pre-trained knowledge.

```text
                    ┌──────────────────────┐
                    │    User Question     │
                    └──────────┬───────────┘
                               │
                               ▼
                 Generate Query Embedding
                               │
                               ▼
                   Semantic Similarity Search
                               │
                               ▼
                Retrieve Relevant Properties
                               │
                               ▼
                 Apply Metadata Filtering
                               │
                               ▼
                Build Context for the LLM
                               │
                               ▼
                    OpenAI GPT-4.1 Mini
                               │
                               ▼
                      Final AI Response
```

---

## 🧠 RAG Implementations

This project contains **three different RAG implementations**, allowing direct comparison between manual development, AI frameworks, and managed vector databases.

| Implementation | Vector Store | Embeddings       | Retrieval           | Purpose                                               |
|----------------|--------------|------------------|---------------------|-------------------------------------------------------|
| Manual RAG     | FAISS        | OpenAI           | Custom Python       | Learn the complete RAG pipeline from first principles |
| LangChain RAG  | FAISS        | OpenAIEmbeddings | LangChain Retriever | Learn framework-based AI development                  |
| Pinecone RAG   | Pinecone     | OpenAI           | Pinecone Query API  | Learn production-ready cloud vector search            |

---

## 🔄 End-to-End Workflow

```text
MongoDB Property Documents
            │
            ▼
Property Formatter
(Convert JSON → Semantic Text)
            │
            ▼
OpenAI Embedding Model
(text-embedding-3-small)
            │
            ▼
      ┌──────────────┬──────────────┬──────────────┐
      │              │              │              |
      ▼              ▼              ▼              ▼
 Manual FAISS    LangChain FAISS   Pinecone        ?
      │              │              │
      └──────────────┴──────────────┘
                     │
                     ▼
          Similarity Search (Top-K)
                     │
                     ▼
         Metadata Filtering (Optional)
                     │
                     ▼
          Context Construction
                     │
                     ▼
             OpenAI GPT-4.1 Mini
                     │
                     ▼
              Final AI Response
```

---

## 🎯 Why Three Implementations?

Rather than stopping after building a single RAG application, this project intentionally explores three different approaches.

### 1️⃣ Manual RAG

Implemented from scratch to understand:

- Embeddings
- Vector indexing
- Similarity search
- Context construction
- Prompt engineering

### 2️⃣ LangChain RAG

Rebuilt using LangChain to understand how AI frameworks simplify:

- Document handling
- Retrieval
- Prompt orchestration
- LLM integration

### 3️⃣ Pinecone RAG

Extended using Pinecone to learn how production AI systems:

- Store vectors in the cloud
- Scale semantic search
- Share vector indexes across multiple application instances
- Support enterprise AI applications

# 🛠 Tech Stack

### Backend
- Python
- FastAPI

### AI / LLM
- OpenAI GPT-4.1 Mini
- OpenAI `text-embedding-3-small`

### Vector Search
- FAISS
- LangChain FAISS VectorStore

### Database
- MongoDB

### Frameworks / Libraries
- LangChain
- NumPy
- PyMongo
- python-dotenv
- Pydantic

---

# 🚀 Features

### 🤖 AI Features

- Retrieval-Augmented Generation (RAG)
- Context-grounded LLM responses
- OpenAI embedding generation
- OpenAI GPT-based answer generation
- Prompt construction using retrieved property context

### 🔎 Retrieval Features

- Natural language semantic property search
- Top-K similarity search
- Manual FAISS vector search
- LangChain FAISS VectorStore retrieval
- Pinecone cloud vector search
- Metadata-based filtering

### 🏠 Real Estate Copilot Features

Users can ask questions such as:

- Show me furnished apartments in Meydan with good rental yield.
- Which properties have the highest ROI?
- Recommend investment-friendly apartments.
- Compare similar properties.
- Show apartments under a specific budget.
- Find apartments in a specific development or area.

### 📊 Hybrid Search Filters

Combines semantic search with structured metadata filtering.

Supported filters include:

- City
- Area
- Development
- Property Type
- Maximum Price
- Minimum Bedrooms

### 🧠 Manual RAG Pipeline

The manual implementation was built to understand the complete RAG flow without relying on framework abstractions.

It includes:

- Property-to-text conversion
- Embedding generation
- FAISS indexing
- Metadata storage
- Similarity search
- Context construction
- LLM response generation

### 🔗 LangChain RAG Pipeline

The LangChain version uses:

- LangChain `Document`
- `OpenAIEmbeddings`
- LangChain FAISS VectorStore
- `ChatPromptTemplate`
- `ChatOpenAI`
- Runnable chain execution

### ☁️ Pinecone RAG Pipeline

The Pinecone version uses:

- Pinecone cloud vector database
- OpenAI-generated embeddings
- Vector upsert with metadata
- Namespace-based property indexing
- Pinecone similarity search
- Pinecone metadata filtering

### ⚙️ Backend Features

- FastAPI REST API
- Swagger UI documentation
- Environment-based configuration
- MongoDB integration
- Modular service structure
- Separate manual, LangChain, and Pinecone implementations
---

# 📂 Project Structure

```text
estate-mind-ai/

├── app/
│   ├── api/
│   │   └── routes/
│   │       └── chat_routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── schemas/
│   │   └── chat_schema.py
│   │
│   ├── services/
│   │   ├── property_formatter.py
│   │   ├── search_state_service.py
│   │   │
│   │   ├── manual_rag/
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   ├── langchain_rag/
│   │   │   ├── vector_store_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   └── pinecone_rag/
│   │       ├── vector_store_service.py
│   │       ├── retrieval_service.py
│   │       └── llm_service.py
│   │
│   └── main.py
│
├── scripts/
│   ├── build_manual_faiss_index.py
│   ├── build_langchain_faiss_index.py
│   ├── build_pinecone_index.py
│   ├── test_manual_retrieval.py
│   └── test_langchain_retrieval.py
│
├── vector_store/
│   └── .gitkeep
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
## ⚙️ How It Works

### 1. Property Formatting

Each MongoDB property document is converted into a clean semantic text format.

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

This improves retrieval quality because embedding models understand natural language better than raw JSON.

---

### 2. Embedding Generation

The formatted property text is converted into vector embeddings using:

```text
text-embedding-3-small
```

Each property becomes a numerical vector that represents its meaning.

---

### 3. FAISS Indexing

The embeddings are stored in FAISS for similarity search.

Manual version:

```text
vector_store/
├── properties.index
└── metadata.json
```

LangChain version:

```text
vector_store/
└── langchain_faiss_index/
    ├── index.faiss
    └── index.pkl
```

These generated vector files are ignored from Git and can be rebuilt using the scripts.

---

### 4. Semantic Retrieval

When a user asks a question, the system:

1. Converts the question into an embedding
2. Searches FAISS for similar property vectors
3. Retrieves the matching property metadata
4. Applies structured filters
5. Sends the retrieved context to the LLM

---

### 5. AI Response Generation

The LLM generates an answer using only the retrieved property context.

This helps reduce hallucinations because the model is grounded with real property data.

---

# 📌 API Endpoints

### Manual RAG Chat

```http
POST /chat/manual
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

---

### LangChain RAG Chat

```http
POST /chat/langchain
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
---

### Pinecone RAG Chat

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
  "sources": [...]
}
```

---

# ▶️ Running the Project

Clone the repository:

```bash
git clone https://github.com/KaveeshaNethmi/estate-mind-ai.git

cd estate-mind-ai
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

MONGO_URI=mongodb://localhost:27017

DB_NAME=your_database_name

COLLECTION_NAME=your_collection_name
```

Build the manual FAISS index:

```bash
python scripts/build_manual_faiss_index.py
```

Build the LangChain FAISS index:

```bash
python scripts/build_langchain_faiss_index.py
```
Build the Pinecone index:

```bash
python scripts/build_pinecone_index.py
```
Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

---

# 🧪 Comparing the Three RAG Implementations

This project intentionally implements the same RAG pipeline in three different ways to understand the trade-offs between building from first principles, using AI frameworks, and using managed cloud vector databases.

### 🛠 Manual RAG

The manual implementation was built completely from scratch to understand every component of the RAG pipeline.

It provides full control over:

- Embedding generation
- Vector creation
- FAISS indexing
- Metadata mapping
- Similarity search
- Context construction
- Prompt engineering
- LLM response generation

This version helped me understand **how Retrieval-Augmented Generation works under the hood** without relying on framework abstractions.

---

### 🔗 LangChain RAG

After completing the manual implementation, I rebuilt the same system using LangChain.

LangChain simplifies development by providing abstractions for:

- Document management
- Embedding generation
- VectorStore integration
- Retrieval
- Prompt templating
- LLM orchestration

This implementation helped me understand **how modern AI frameworks accelerate development while hiding much of the underlying complexity**.

---

### ☁️ Pinecone RAG

The third implementation replaces the local FAISS vector database with **Pinecone**, a managed cloud vector database commonly used in production AI systems.

This implementation demonstrates:

- Cloud-hosted vector storage
- Persistent vector indexes
- Metadata-based filtering
- Scalable semantic search
- Production-style vector retrieval

This version helped me understand the transition from a **locally hosted RAG system** to a **cloud-native architecture** that can scale across multiple application instances.

---

### 📌 Key Takeaways

Building the same project in three different ways gave me a much deeper understanding of modern AI application development.

- **Manual RAG** taught me how every component works internally.
- **LangChain** showed how frameworks improve developer productivity.
- **Pinecone** demonstrated how vector databases are managed in production environments.

Rather than learning only a framework, this approach helped me understand the complete evolution of a Retrieval-Augmented Generation system—from first principles to a production-ready architecture.

---

# 📖 What I Learned

Building EstateMind AI helped me gain hands-on experience in designing and implementing production-style Retrieval-Augmented Generation (RAG) systems from first principles.

### AI & Machine Learning

- Retrieval-Augmented Generation (RAG)
- OpenAI Embeddings
- Semantic Search
- Vector Representations
- Prompt Engineering
- Context Grounding
- Hybrid Retrieval
- Metadata Filtering

### Vector Databases

- FAISS
- Pinecone
- Similarity Search
- Nearest-Neighbor Search
- Vector Indexing
- Cloud Vector Databases

### AI Frameworks

- LangChain
- Document Management
- VectorStore Integration
- Prompt Templates
- Runnable Chains

### Backend Engineering

- FastAPI
- REST API Development
- MongoDB Integration
- Environment-based Configuration
- Modular Project Architecture
- Production-style Service Design

### Key Takeaways

Through this project, I learned:

- How Retrieval-Augmented Generation works internally.
- How embeddings transform text into semantic vector representations.
- How vector databases retrieve information based on meaning rather than exact keywords.
- The differences between building a RAG pipeline manually versus using AI frameworks like LangChain.
- The advantages of cloud-hosted vector databases such as Pinecone for production AI applications.
- How to design scalable AI backend services using FastAPI and modular architecture.

---

# 🚀 Roadmap

This project will continue to evolve as I explore more advanced AI engineering concepts.

### Phase 1 ✅ (Completed)

- ✅ Manual RAG Implementation
- ✅ LangChain RAG Implementation
- ✅ Pinecone Integration
- ✅ Hybrid Retrieval
- ✅ FastAPI REST API
- ✅ Metadata Filtering

### Phase 2 ✅ (Completed)

- ✅ Conversational Memory
- ✅ Conversation History
- ✅ State-aware Chat Retrieval

### Phase 3 🚧 (Next)

- ⏳ Natural Language Filter Extraction
- ⏳ Advanced Multi-turn Chat
- ⏳ Query Rewriting

### Phase 4

- ⏳ Source Citations
- ⏳ Reranking Models
- ⏳ Confidence Scores

### Phase 5

- ⏳ Streaming Responses
- ⏳ Background Indexing Jobs
- ⏳ Incremental Data Ingestion
- ⏳ Async Processing

### Phase 6

- ⏳ Authentication & Authorization
- ⏳ React Frontend
- ⏳ Docker
- ⏳ CI/CD Pipeline
- ⏳ Cloud Deployment (AWS/GCP)

### Long-Term Vision

Transform EstateMind AI into a production-ready AI Copilot capable of assisting users with:

- Real estate investment analysis
- Property recommendations
- Portfolio comparison
- Market insights
- Conversational property search
- Intelligent decision support

## 👨‍💻 Author

**Kaveesha Abeynayake**

Backend-focused Software Engineer transitioning into AI Engineering.

Currently exploring:

- Retrieval-Augmented Generation
- LLM Applications
- AI Agents
- Vector Databases
- Production AI Systems