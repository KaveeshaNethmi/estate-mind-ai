# 🏡 EstateMind AI - Real Estate AI Copilot

A production-style **Retrieval-Augmented Generation (RAG)** application that allows users to interact with a real estate property database using natural language.

EstateMind AI retrieves relevant property data from a vector database, grounds the response with real property information, and generates context-aware answers using an LLM.

This project includes **two RAG implementations**:

1. **Manual RAG Implementation**  
   Built from first principles using OpenAI Embeddings, FAISS, NumPy, and FastAPI.

2. **LangChain RAG Implementation**  
   Rebuilt using LangChain to compare framework-based development with the manual approach.

---

## 🚀 Features

### 🔎 Semantic Property Search
- Natural language property search
- OpenAI embedding generation
- FAISS vector similarity search
- Top-K relevant property retrieval

### 🏠 Real Estate AI Copilot
Users can ask questions such as:

- Show me furnished apartments in Meydan with good rental yield.
- Which properties have the highest ROI?
- Recommend investment-friendly apartments.
- Compare similar properties.
- Show apartments under a specific budget.

### 📊 Hybrid Retrieval
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

---

## 🏗 Architecture

```text
                         User Question
                               │
                               ▼
                     Generate Query Embedding
                               │
                               ▼
                      FAISS Similarity Search
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
                    OpenAI GPT Model
                               │
                               ▼
                         Final AI Response
```

---

## 🛠 Tech Stack

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

## 📂 Project Structure

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
│   │   │
│   │   ├── manual_rag/
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   └── langchain_rag/
│   │       ├── vector_store_service.py
│   │       ├── retrieval_service.py
│   │       └── llm_service.py
│   │
│   └── main.py
│
├── scripts/
│   ├── build_manual_faiss_index.py
│   ├── build_langchain_faiss_index.py
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
```

---

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

## 📌 API Endpoints

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

Example response:

```json
{
  "answer": "...",
  "sources": [...]
}
```

---

## ▶️ Running the Project

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

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

---

## 🧪 Manual RAG vs LangChain RAG

### Manual RAG

The manual implementation gives full control over:

- Embedding generation
- Vector creation
- FAISS indexing
- Metadata mapping
- Similarity search
- Context construction

This helped me understand how RAG works internally.

### LangChain RAG

The LangChain implementation reduces boilerplate and improves developer productivity by abstracting:

- Document handling
- VectorStore management
- Retriever logic
- Prompt chaining
- LLM invocation

This helped me understand how frameworks simplify production AI development.

---

## 📖 What I Learned

This project helped me gain practical experience with:

- Retrieval-Augmented Generation
- OpenAI Embeddings
- Vector Databases
- FAISS
- LangChain
- Semantic Search
- Hybrid Retrieval
- Prompt Engineering
- Context Grounding
- FastAPI
- MongoDB Integration
- Production-style AI Backend Development

---

## 🚀 Future Improvements

- Pinecone integration
- Conversational memory
- Property comparison
- Reranking models
- Streaming responses
- Authentication
- Conversation history
- Citation support
- Multi-agent workflows
- React frontend

---

## 📚 Why I Built Both Versions

Most tutorials start directly with LangChain.

For this project, I first built the RAG pipeline manually to understand the fundamentals.

Then I rebuilt the same system using LangChain to understand how framework abstractions improve development speed and maintainability.

This gave me a clearer understanding of both:

- How RAG works under the hood
- How modern AI frameworks simplify implementation

---

## 👨‍💻 Author

**Kaveesha Abeynayake**

Backend-focused Software Engineer transitioning into AI Engineering.

Currently exploring:

- Retrieval-Augmented Generation
- LLM Applications
- AI Agents
- Vector Databases
- Production AI Systems