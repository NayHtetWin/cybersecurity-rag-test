import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import shutil

# --- Configuration ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "dataset")
DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")

def ingest_documents():
        """Load PDFs, chunk them, 
        and store embeddings in ChromaDB."""
    # Load Documents
    print("📂 Loading documents...")
    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(DATA_PATH, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    
    print(f"Loaded {len(documents)} pages from {len(os.listdir(DATA_PATH))} PDF files.")

    # CLEANUP: Remove existing vector DB 
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print(f"🗑️ Cleared existing database at {DB_PATH}")

    # Split Text (Chunking)
    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    print("Creating embeddings and storing in Vector DB...")
    
    #Use a standard, efficient HuggingFace model for embeddings (runs locally)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create the vector store
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print("Success! Vector Database created at ./chroma_db")

if __name__ == "__main__":
    ingest_documents()