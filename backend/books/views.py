from typing import cast, List

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books
from .ai_utils import generate_summary
from .embeddings import store_embedding, query_books
from .gemini_utils import generate_answer
from django.db import models


qa_cache = {}

# GET all books
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# POST add single book
@api_view(['POST'])
def add_book(request):
    data = request.data.copy()

    # Generate summary safely
    data['summary'] = generate_summary(data.get('description', ''))

    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        book_instance = cast(Book, serializer.save())  # type-safe

        # Store embedding
        if book_instance.description:
            store_embedding(book_instance.id, book_instance.description)

        return Response(serializer.data)

    return Response(serializer.errors)


# POST scrape + store books
@api_view(['POST'])
def scrape_and_store(request):
    books_data = scrape_books()

    saved_books = []

    for book in books_data:
        serializer = BookSerializer(data=book)

        if serializer.is_valid():
            saved = cast(Book, serializer.save())  

            # Store embedding safely
            if saved.description:
                store_embedding(saved.id, saved.description)

            saved_books.append(serializer.data)

    return Response(saved_books)


# POST RAG query
@api_view(['POST'])
def ask_question(request):
    question: str = request.data.get("question", "")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    docs = query_books(question) or []

    books = Book.objects.all()

    structured_context = "\n".join([
        f"Title: {b.title}, Rating: {b.rating}, Description: {b.description}"
        for b in books
    ])

    # Combine both
    context = structured_context

    answer = generate_answer(question, context)

    return Response({
        "question": question,
        "answer": answer,
        "sources": docs
    })