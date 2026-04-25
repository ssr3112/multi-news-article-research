from app_core.llm.gemini_client import get_gemini_client

def generate_answer(question, contexts):
    client = get_gemini_client()

    combined_context = "\n\n".join(
        [f"Title: {item['title']}\nContent: {item['chunk']}" for item in contexts]
    )

    prompt = f"""
    Answer the question using only the context below.
    If the answer is not found in the context, say:
    "The answer is not available in the provided articles."

    Context:
    {combined_context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text