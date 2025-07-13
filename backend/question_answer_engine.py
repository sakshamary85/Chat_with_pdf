from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os
import hashlib

CHROMA_DB_DIR = "./chroma_db"

def get_file_hash(text):
    """Generate SHA256 hash of the document content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def prepare_retriever(text, persist=True):
    # Generate unique sub-directory for this document
    file_hash = get_file_hash(text)
    db_path = os.path.join(CHROMA_DB_DIR, file_hash)

    if os.path.exists(os.path.join(db_path, "index")):
        # Load existing vectorstore if already indexed
        vectordb = Chroma(
            persist_directory=db_path,
            embedding_function=OllamaEmbeddings(model="nomic-embed-text")
        )
    else:
        # Split text into manageable chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
        chunks = splitter.create_documents([text])

        # Create vectorstore with fast embedding model
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=db_path if persist else None
        )

    return vectordb.as_retriever(search_kwargs={"k": 2})

def answer_question(question, retriever):
    llm = OllamaLLM(model="mistral")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)
    return chain.invoke({"query": question})
