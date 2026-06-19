import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question):

    prompt = f"""
    You are CampusConnect AI, a college information assistant.

    Answer student questions politely and clearly.

    Question:
    {question}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"