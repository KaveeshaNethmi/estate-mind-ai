# 🏡 EstateMind AI - Real Estate AI Copilot

A production-style **Retrieval-Augmented Generation (RAG)** application that enables users to interact with a real estate property database using natural language.

Instead of relying solely on an LLM's internal knowledge, EstateMind AI retrieves relevant property data from a vector database, grounds the response with real property information, and generates accurate, context-aware answers.

This project was intentionally built **without LangChain** to understand the complete RAG pipeline from first principles before using higher-level frameworks.

---

# 🚀 Features

## 🔎 Semantic Property Search
- Natural language search using OpenAI embeddings
- Retrieve semantically similar properties
- Vector similarity search using FAISS

## 🏠 Real Estate AI Copilot
Ask questions such as:

- Show me furnished apartments in Meydan with good rental yield.
- Which properties have the highest ROI?
- Recommend investment-friendly apartments.
- Compare similar properties.

## 📊 Hybrid Retrieval
Supports semantic search together with structured filtering.

Example filters:

- Property Type
- City
- Area
- Development
- Maximum Price
- Minimum Bedrooms

## 🧠 Retrieval-Augmented Generation (RAG)

The application performs:

1. Property formatting
2. Embedding generation
3. Vector search
4. Context retrieval
5. LLM response generation

to produce grounded AI answers.

---

# 🏗 Architecture

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
                    OpenAI GPT-4.1 Mini
                               │
                               ▼
                         Final AI Response
```

---

# 🛠 Tech Stack

### Backend

- Python
- FastAPI

### AI

- OpenAI GPT-4.1 Mini
- OpenAI text-embedding-3-small

### Vector Search

- FAISS

### Database

- MongoDB

### Other

- NumPy
- PyMongo
- python-dotenv

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
│   │   ├── embedding_service.py
│   │   ├── vector_store_service.py
│   │   ├── retrieval_service.py
│   │   └── llm_service.py
│   │
│   └── main.py
│
├── scripts/
│   ├── build_faiss_index.py
│   └── test_retrieval.py
│
├── vector_store/
│   ├── properties.index
│   └── metadata.json
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ How It Works

## 1. Property Formatting

Each MongoDB property document is converted into a semantic description.

Example:

```
1-bedroom furnished apartment located in Meydan, Dubai.

Price: 1,050,700 AED

Rental Yield: 5.1%

ROI (15 Years): 75.4%

Amenities:
Shared Spa
Restaurants
Public Parking
Children's Play Area
```

---

## 2. Embedding Generation

The formatted text is converted into vector embeddings using:

```
text-embedding-3-small
```

---

## 3. FAISS Indexing

Embeddings are stored inside a FAISS index.

Metadata is stored separately for fast retrieval.

```
Vector
        ↓
FAISS Index

Metadata
        ↓
metadata.json
```

---

## 4. Semantic Retrieval

User question:

```
Show me furnished apartments in Meydan with good rental yield.
```

↓

Generate query embedding

↓

Retrieve Top-K similar properties

↓

Apply metadata filters

↓

Pass retrieved context to the LLM.

---

## 5. AI Response

The LLM generates a grounded response using only the retrieved property information.

---

# 📌 API Endpoints

## Chat

```
POST /chat
```

Example Request

```json
{
    "question": "Show me furnished apartments in Meydan with good rental yield.",
    "top_k": 5,
    "development": "Meydan",
    "max_price": 1200000
}
```

Example Response

```json
{
    "answer": "...",
    "sources": [...]
}
```

---

# ▶️ Running the Project

Clone the repository

```bash
git clone <repository-url>

cd estate-mind-ai
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create

```
.env
```

```env
OPENAI_API_KEY=your_api_key

MONGO_URI=...

DB_NAME=...

COLLECTION_NAME=...
```

Build the FAISS index

```bash
python scripts/build_faiss_index.py
```

Start the server

```bash
uvicorn app.main:app --reload
```

Open Swagger

```
http://localhost:8000/docs
```

---

# 📖 What I Learned

This project helped me gain practical experience with:

- Retrieval-Augmented Generation (RAG)
- OpenAI Embeddings
- Semantic Search
- Vector Databases
- FAISS
- Hybrid Retrieval
- Prompt Engineering
- Context Grounding
- FastAPI
- MongoDB Integration
- Production-style AI Backend Development

---

# 🚀 Future Improvements

- LangChain implementation
- Pinecone integration
- Conversational memory
- Property comparison
- Reranking models
- Streaming responses
- Authentication
- Conversation history
- Citation support
- Multi-agent workflows

---

# 📚 Why Build Without LangChain?

Most RAG tutorials rely heavily on LangChain, which abstracts away much of the underlying logic.

This project intentionally implements the RAG pipeline manually to gain a deeper understanding of:

- Embedding generation
- Vector indexing
- Similarity search
- Retrieval
- Context construction
- LLM prompting

A future version of this project will rebuild the same architecture using LangChain to compare abstraction, maintainability, and developer productivity.

---

# 👨‍💻 Author

**Kaveesha Abeynayake**

Backend focused Software Engineer transitioning into AI Engineering.

Currently exploring:

- Retrieval-Augmented Generation (RAG)
- LLM Applications
- AI Agents
- Vector Databases
- Production AI Systems