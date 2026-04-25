from app_core.llm.gemini_client import get_gemini_client

def summarize_text(text):
    client = get_gemini_client()

    prompt = f"""
    Summarize the following news article in simple and clear language.
    Keep the summary around 5 to 6 lines.
    
    Article:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text