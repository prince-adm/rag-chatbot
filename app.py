import os
import gradio as gr
from rag import get_response as get_rag_response
from llm import get_llm_response
from indexer import create_vector_db

# --- FINAL FIX: Check for and create the database on startup ---
DB_FAISS_PATH = "vectordb/"
if not os.path.exists(DB_FAISS_PATH):
    print("Vector database not found. Creating it now...")
    create_vector_db()
    print("Database created successfully.")
else:
    print("Vector database already exists.")
# ----------------------------------------------------------------

print("Starting the Gradio application...")

def chatbot_response(message, history):
    """
    The main function that powers the chatbot.
    """
    print(f"Received query: {message}")

    # 1. Retrieve context
    print("Step 1: Retrieving context...")
    context = get_rag_response(message)

    # 2. Generate a final answer
    print("Step 2: Generating final answer...")
    final_answer = get_llm_response(message, context)

    print(f"Final answer: {final_answer}")
    return final_answer

# Create the Gradio web interface
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="Advanced RAG Chatbot",
    description="This chatbot uses a cloud-hosted LLM and a local knowledge base to answer questions."
)

# Launch the interface
if __name__ == "__main__":
    iface.launch()