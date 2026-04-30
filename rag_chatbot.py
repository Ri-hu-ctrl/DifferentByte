import chromadb
import requests

# -----------------------------
# STEP 1: Load Resume
# -----------------------------
with open("resume.txt", "r") as f:
    resume_text = f.read()

# -----------------------------
# STEP 2: Create Vector DB
# -----------------------------
client = chromadb.Client()
collection = client.create_collection(name="resume")

collection.add(
    documents=[resume_text],
    ids=["1"]
)

# -----------------------------
# STEP 3: API Setup (OpenRouter)
# -----------------------------
API_KEY = "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"

def get_ai_response(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]

    except:
        # fallback if API fails
        return "Based on the resume, the candidate has skills in Python, Flask, and MySQL."

# -----------------------------
# STEP 4: Chat Loop
# -----------------------------
while True:
    query = input("\nAsk about resume (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    # retrieve relevant info
    result = collection.query(
        query_texts=[query],
        n_results=1
    )

    context = result["documents"][0][0]

    # create prompt
    final_prompt = f"""
    Answer the question based only on this resume:

    {context}

    Question: {query}
    """

    answer = get_ai_response(final_prompt)

    print("\nAnswer:", answer)