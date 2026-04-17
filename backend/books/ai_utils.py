from transformers import pipeline

summarizer = pipeline("summarization")

def generate_summary(text):
    if not text:
        return ""

    try:
        summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
        return summary[0]['summary_text']
    except:
        return text[:100]  # fallback