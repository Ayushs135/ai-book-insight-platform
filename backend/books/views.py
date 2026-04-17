from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def scrape_and_store(request):
    books_data = scrape_books()

    saved_books = []
    for book in books_data:
        serializer = BookSerializer(data=book)
        if serializer.is_valid():
            serializer.save()
            saved_books.append(serializer.data)

    return Response(saved_books)