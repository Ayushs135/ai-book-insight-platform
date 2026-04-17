from django.urls import path
from .views import get_books, add_book, scrape_and_store

urlpatterns = [
    path('books/', get_books),
    path('books/add/', add_book),
    path('books/scrape/', scrape_and_store),
]