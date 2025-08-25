import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/"
DB_FAISS_PATH = "vectordb/"

def create_vector_db():
    """
    Loads documents from the data path, splits them into chunks, 
    creates embeddings, and saves them to a FAISS vector store.
    """
    loader = TextLoader(os.path.join(DATA_PATH, "info.txt"))
    documents = loader.load()
    print("Successfully loaded the document.")
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split the document into {len(chunks)} chunks.")
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    print("Embeddings model loaded.")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database created successfully and saved in '{DB_FAISS_PATH}'")
if __name__ == "__main__":
    create_vector_db()