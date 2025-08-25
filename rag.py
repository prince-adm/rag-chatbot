from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DB_FAISS_PATH = "vectordb/"

def get_response(query):
    """
    Searches the vector database for the most relevant information based on a user's query.
    """
    print("Loading the vector database...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    print(f"Searching for relevant documents for the query: '{query}'")
    
    docs = db.similarity_search(query)
    
    
    if docs:
        context = "\n".join([doc.page_content for doc in docs])
        return context
    else:
        return "Sorry, I couldn't find any information on that."


if __name__ == "__main__":
    
    test_query = "What is Gemini Pro?"
    
    print(f"Testing the RAG system with query: '{test_query}'")
    
    response_context = get_response(test_query)
    
    print("\n--- Found Context ---")
    print(response_context)
    print("--------------------")