import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DB_PATH = os.path.join(PROJECT_ROOT, "chroma_db")
MODEL_NAME = "qwen2.5"    

def get_rag_chain():
    """
    Creates the RAG chain: Retrieval -> Prompt -> LLM -> Output
    """
    # Load the Vector DB
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    
    # Setup Retriever
    # fetch the top 5 most relevant chunks
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    # Setup Local LLM (Ollama)
    llm = ChatOllama(model=MODEL_NAME)

    # Define the Strict Prompt 
    template = """
    You are a Cybersecurity RAG Assistant. 
    You must answer the user's question strictly based ONLY on the provided context below.
    
    Rules:
    1. Do NOT use outside knowledge. Omit from introduction with outside knowledge.
    2. If the answer is not in the context, say "I cannot answer this based on the provided documents."
    3. You must cite the source file for every key statement using the format: [Source: filename, Page: page number].
    
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer:
    """
    
    prompt = ChatPromptTemplate.from_template(template)


    def format_docs(docs):
        formatted_docs = []
        for d in docs:
            # Get the full path
            source_path = d.metadata.get('source', 'Unknown')
            
            # Extract ONLY the filename
            filename = os.path.basename(source_path) 
            
            # Get page number (start at 1 instead of 0)
            page_num = d.metadata.get('page', -1) + 1
            
            # Format the string
            formatted_docs.append(
                f"[Source: {filename}, Page: {page_num}]\n{d.page_content}"
            )
            
        return "\n\n".join(formatted_docs)
        
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def ask_question(query):
    print(f" Question: {query}")
    print("..." * 10)
    
    try:
        chain = get_rag_chain()
        response = chain.invoke(query)
        print("\n Answer:\n")
        print(response)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test Question
    ask_question("What is Broken Access Control according to OWASP?")