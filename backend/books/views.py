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
            saved = serializer.save()
            saved_books.append(serializer.data)
        else:
            print("❌ Serializer error:", serializer.errors) 

    return Response(saved_books)


# POST RAG query
@api_view(['POST'])
def ask_question(request):
    question: str = request.data.get("question", "")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    books = Book.objects.all()[:10]

    context = "\n".join([
        f"Title: {b.title}, Author: {b.author}, Rating: {b.rating}, Description: {b.description}"
        for b in books
    ])

    answer = generate_answer(question, context)

    return Response({
        "question": question,
        "answer": answer,
        "type": "gemini"
    })