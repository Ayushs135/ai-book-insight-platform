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

IMPORTANT:
- Always complete the sentence fully
- Do NOT stop mid-sentence
- Do NOT use "..."
- Mention full book title
- Explain recommendation in 1–2 sentences
- If asking for summary, provide a concise summary in 2–3 sentences from the description

If recommending:
- Choose the highest rated book

If answer not found:
- Say "Not found in data"

DATA:
{context}

QUESTION:
{question}

FULL ANSWER:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.4,
                "max_output_tokens": 350
            }
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No answer generated"

    except Exception as e:
        print("Gemini error:", e)
        return "Error generating answer"