from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""
You are a helpful AI assistant.

Answer the question using ONLY the provided data.

IMPORTANT RULES:
- Always give a COMPLETE sentence (not short phrases)
- Mention FULL book title (do NOT truncate)
- Include rating if relevant
- If comparing (highest, lowest, cheapest), clearly state the result
- Be precise but NOT overly short
- Do NOT use "..." or cut sentences
- If answer not present, say "Not found in data"

Data:
{context}

Question:
{question}

Answer:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.3,
                "max_output_tokens": 200
            }
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No answer generated"

    except Exception as e:
        print("Gemini error:", e)
        return "Error generating answer"