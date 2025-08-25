from flask import Flask, request, jsonify, render_template
from rag import get_response as get_rag_response
from llm import get_llm_response

# Initialize the Flask application
app = Flask(__name__)

# This is the main route for our chatbot's user interface
@app.route("/")
def index():
    # This will render the index.html file from the 'templates' folder
    return render_template("index.html")

# This is the API endpoint that our frontend will call
@app.route("/get_answer", methods=["POST"])
def get_answer():
    # Get the user's question from the request
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    print(f"Received query: {query}")

    # 1. Retrieve context using our RAG system
    print("Step 1: Retrieving context...")
    context = get_rag_response(query)

    # 2. Generate a final answer using the LLM API
    print("Step 2: Generating final answer...")
    final_answer = get_llm_response(query, context)
    
    print(f" {final_answer}")

    # 3. Send the answer back to the frontend
    return jsonify({"answer": final_answer})

if __name__ == "__main__":
    # Run the Flask app on our new working port
    app.run(debug=True, port=8080)