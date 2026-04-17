from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books
from .ai_utils import generate_summary
from .embeddings import store_embedding
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .embeddings import query_books

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_book(request):
    data = request.data.copy()

    data['summary'] = generate_summary(data.get('description', ''))

    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        book_instance = serializer.save()
        store_embedding(book_instance.id, book_instance.description)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def scrape_and_store(request):
    books_data = scrape_books()

    saved_books = []
    for book in books_data:
        serializer = BookSerializer(data=book)
        if serializer.is_valid():
            saved = serializer.save()
            store_embedding(saved.id, saved.description)
            saved_books.append(serializer.data)

    return Response(saved_books)

@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")

    docs = query_books(question)

    context = " ".join([doc for sublist in docs for doc in sublist])

    # Simple response (LLM can be added later)
    return Response({
        "question": question,
        "answer": context,
        "sources": docs
    })