import gradio as gr
from rag import get_response as get_rag_response
from llm import get_llm_response

print("Starting the application...")

def chatbot_response(message, history):
    """
    The main function that powers the chatbot.
    It takes a user message and the chat history, and returns the AI's response.
    """
    print(f"Received query: {message}")

    # 1. Retrieve context using our RAG system
    print("Step 1: Retrieving context...")
    context = get_rag_response(message)

    # 2. Generate a final answer using the LLM API
    print("Step 2: Generating final answer...")
    final_answer = get_llm_response(message, context)
    
    print(f" {final_answer}")
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