from google import genai
from google.genai.errors import ClientError
 
from app.core.config import settings
 
client = genai.Client(

    api_key=settings.GEMINI_API_KEY

)
 
 
def ask_gemini(question: str, context: str):
 
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
 
    try:

        response = client.models.generate_content(

            model=settings.GEMINI_MODEL,

            contents=prompt

        )
 
        return response.text
 
    except ClientError as e:

        print("Gemini API Error:", e)

        return "Gemini API quota exceeded. Please try again later."
 
    except Exception as e:

        print("Unexpected Error:", e)

        return "An unexpected error occurred while generating the answer."
 
    except ClientError as e:

            print("Gemini API Error:", e)

            return "Gemini API quota exceeded. Please try again later."
    
    except Exception as e:

        print("Unexpected Error:", e)

        return "An unexpected error occurred while generating the answer."
