from transformers import pipeline
from typing import Any, List, Dict, cast

summarizer = None  # lazy load

def generate_summary(text: str) -> str:
    global summarizer

    if not text:
        return ""

    try:
        if summarizer is None:
            summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6"
            )  # type: ignore

        raw_result = summarizer(
            text,
            max_length=50,
            min_length=20,
            do_sample=False
        )

        result = cast(List[Dict[str, Any]], raw_result)

        if result and isinstance(result, list):
            return str(result[0].get("summary_text", ""))

        return text[:100]

    except Exception as e:
        print("Summary error:", e)
        return text[:100]