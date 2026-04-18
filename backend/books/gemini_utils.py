from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question: str, context: str) -> str:
    try:
        prompt = f"""
        You are a helpful AI assistant.

        Answer the question using ONLY the provided context.
        IMPORTANT:
        - If asked about highest rating, compare ratings
        - If asked about cheapest, compare price
        - Be precise and concise. Use only the information given in the context.
        If the answer is not present, say "Not found in data".

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text if response.text else "No answer generated"

    except Exception as e:
        print("Gemini error:", e)
        return "Error generating answer"