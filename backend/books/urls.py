from django.urls import path
from .views import (
    get_books,
    add_book,
    scrape_and_store,
    ask_question,
    get_book_detail,
    get_similar_books
)

urlpatterns = [
    path('books/', get_books),
    path('books/add/', add_book),
    path('books/scrape/', scrape_and_store),
    path('books/<int:pk>/', get_book_detail),
    path('books/<int:pk>/recommend/', get_similar_books),
    path('ask/', ask_question),
]