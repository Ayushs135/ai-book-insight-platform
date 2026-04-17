from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()
collection = client.get_or_create_collection(name="books")

def store_embedding(book_id, text):
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(book_id)]
    )

def query_books(question):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results['documents']