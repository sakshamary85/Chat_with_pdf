# AI PDF Assistant 🧠📄
## Introduction
This is a local Generative AI Assistant that can understand, summarize, and question any uploaded PDF/TXT document. It supports deep document comprehension, logic-based Q&A, and interactive challenges — all running **locally** using open-source models via Ollama.

---

## 🔧 Features

- Upload PDF or TXT file
- Auto-summary (≤150 words)
- Ask-anything mode with context understanding
- Challenge Me mode (3 logic/comprehension questions)
- Memory handling for follow-up questions
- Answer highlighting with source references
- Fully local: no OpenAI API required

---

## 🧩 Tech Stack
- Frontend: Streamlit
- Backend: Python, LangChain
- Embeddings: OllamaEmbeddings (Mistral)
- Vector DB: ChromaDB (local)
- LLM: Mistral via Ollama (100% local)

---

## 📦 Requirements
Install the required Python packages with:

```bash
pip install -r requirement.txt
```

---

## ⚙️ Setup Instructions

1. **Install Ollama (if not already installed)**  
   https://ollama.com/download

2. **Run Mistral locally**
   ```bash
   ollama run mistral
   ollama run nomic-embed-text

3. **Clone the repository**
   ```bash
   https://github.com/AryaAnuj2004/SmartAI-Document-Assistant

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt

5. **Start the app**
   ```bash
   streamlit run app.py

---

## 🧠 Architecture & Reasoning Flow
```
                                 ┌──────────────┐
                                 │  Upload File │ ←────────────┐
                                 └─────┬────────┘              │
                                       │                       │
                                       ▼                       │
                          ┌────────────────────────┐           │
                          │ Text Extraction &      │           │
                          │ Chunking (LangChain)   │           │
                          └────────┬───────────────┘           │
                                   ▼                           │
                       ┌─────────────────────┐                 │
                       │ Embeddings (Ollama) │                 │
                       └────────┬────────────┘                 │
                                ▼                              │
                      ┌──────────────────────┐     User selects mode
                      │ Vectorstore (Chroma) │ ───────────────► Ask / Challenge
                      └─────────┬────────────┘                 │
                                ▼                              ▼
                 ┌──────────────────────┐       ┌───────────────────────────────────────────────────┐
                 │  RetrievalQA Chain   │       │                Challenge Mode                     │
                 │ (Mistral via Ollama) │       │(Question Generation + Evaluation + Justification) │
                 └────────┬─────────────┘       └───────────────────────┬───────────────────────────┘
                          ▼                                             ▼
                    Answers with                             Justified feedback + source
                   source references
```
---

#### ⚠️ I implemented the core logic in Python using modular backend files, and built the UI + interaction logic using Streamlit to provide a seamless and responsive user experience, as per the requirement.

---
## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
