import requests

# !!! IMPORTANT: PASTE THE NGROK URL FROM YOUR COLAB OUTPUT HERE !!!
# Make sure it ends with /generate
MODEL_API_URL = "https://3c0954b593a9.ngrok-free.app/generate" 
def get_llm_response(query, context):
    """
    Generates a response by calling our new Colab-hosted API.
    """
    payload = {
        "query": query,
        "context": context
    }
    
    print("Sending request to our Colab server...")
    try:
        response = requests.post(MODEL_API_URL, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return result.get("answer", "Sorry, something went wrong.")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Colab API: {e}")
        return "Sorry, I could not connect to the AI model on the cloud."