from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def ask_gemini(
    question: str,
    context: str
):

    prompt = f"""
You are an AI Knowledge Assistant.

Answer ONLY using the provided document context.

If the answer is not available in the context, reply exactly:

I couldn't find this information in the uploaded documents.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt
    )

    return response.text