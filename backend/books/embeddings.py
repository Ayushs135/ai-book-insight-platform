from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()
collection = client.get_or_create_collection(name="books")


# Store embedding with metadata
def store_embedding(book_id, text, title=""):
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(book_id)],
        metadatas=[{
            "book_id": str(book_id),
            "title": title
        }]
    )


# Query similar books properly
def query_books(question):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Return IDs instead of text
    ids = results.get("ids", [[]])[0]

    return ids