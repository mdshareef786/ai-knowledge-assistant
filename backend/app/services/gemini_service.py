from app.ai.gemini_service import ask_gemini
import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel(settings.GEMINI_MODEL)


class GeminiService:

    @staticmethod
    def ask(
        question: str,
        context: str
    ):

        return ask_gemini(
            question=question,
            context=context
        )