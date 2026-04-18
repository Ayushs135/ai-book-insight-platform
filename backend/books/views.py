from typing import cast

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books
from .ai_utils import generate_summary
from .embeddings import store_embedding, query_books
from .gemini_utils import generate_answer


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

    data['summary'] = generate_summary(data.get('description', ''))

    serializer = BookSerializer(data=data)

    if serializer.is_valid():
        book_instance = cast(Book, serializer.save())

        # FIXED: correct variable
        if book_instance.description:
            store_embedding(
                book_instance.id,
                book_instance.description,
                book_instance.title
            )

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# POST scrape + store books
@api_view(['POST'])
def scrape_and_store(request):
    books_data = scrape_books()

    saved_books = []

    for book in books_data:
        serializer = BookSerializer(data=book)

        if serializer.is_valid():
            saved = serializer.save()

            # IMPORTANT: store embeddings here
            if saved.description:
                store_embedding(
                    saved.id,
                    saved.description,
                    saved.title
                )

            saved_books.append(serializer.data)

        else:
            print(" Serializer error:", serializer.errors)

    return Response(saved_books)


# POST RAG query
@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question", "")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    # Use top books as context
    books = Book.objects.order_by('-rating')[:5]

    context = "\n".join([
        f"Title: {b.title}, Author: {b.author}, Rating: {b.rating}, Description: {b.description}"
        for b in books
    ])

    answer = generate_answer(question, context)

    sources = [
        {
            "id": b.id,
            "title": b.title
        }
        for b in books
    ]

    return Response({
        "question": question,
        "answer": answer,
        "sources": sources
    })


# GET single book detail
@api_view(['GET'])
def get_book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)


# GET similar books
@api_view(['GET'])
def get_similar_books(request, pk):
    try:
        book = Book.objects.get(pk=pk)

        similar_ids = query_books(book.description) or []

        print("SIMILAR IDS:", similar_ids)

        similar_ids = list(set([
            int(i) for i in similar_ids
            if isinstance(i, str) and i.isdigit()
        ]))

        if not similar_ids:
            print("FALLBACK TRIGGERED")
            similar_books = Book.objects.exclude(id=book.id).order_by('-rating')[:3]
        else:
            similar_books = Book.objects.filter(id__in=similar_ids).exclude(id=book.id)[:3]

        serializer = BookSerializer(similar_books, many=True)
        return Response(serializer.data)

    except Exception as e:
        print("SIMILAR ERROR:", e)
        return Response([], status=200)