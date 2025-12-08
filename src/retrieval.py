import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- Config Path ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")

def test_retrieval():
    """
    Loads the Vector DB and performs a test search to verify data ingestion.
    """
    print("Loading Vector Database...")
    
    # SAME embedding model as ingestion
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load the persisted database
    vector_db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_function
    )
    
    # Test Query
    query = "What are the requirements for password rotation?"
    
    print(f"🔍 Testing Query: '{query}'\n")
    
    # Perform Similarity Search (Retrieve top 3 results)
    results = vector_db.similarity_search(query, k=3)
    
    if not results:
        print("No results found. Something went wrong with ingestion.")
        return

    print(f"Found {len(results)} relevant documents:\n")
    
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content Preview: {doc.page_content[:300]}...") # Show first 300 chars
        print("-" * 30)

if __name__ == "__main__":
    test_retrieval()