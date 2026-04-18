from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""
You are a smart AI assistant for a book platform.

Answer using ONLY the provided data.

STRICT RULES:
- Always complete your sentence fully
- NEVER stop mid-sentence
- DO NOT use "..."
- Use full book titles
- Keep answer 2–3 sentences

If summarizing:
- Give a complete explanation

If recommending:
- Choose highest rated book and explain why

If answer not found:
- Say "Not found in data"

DATA:
{context}

QUESTION:
{question}

FINAL COMPLETE ANSWER:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 500
            }
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No answer generated"

    except Exception as e:
        print("Gemini error:", e)
        return "Error generating answer"