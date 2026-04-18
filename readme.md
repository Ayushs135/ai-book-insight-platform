# AI Book Insight Platform

## Overview

AI Book Insight Platform is a full-stack web application that scrapes
book data, stores it in a backend database, and enables intelligent
querying using a Retrieval-Augmented Generation (RAG) pipeline. The
system allows users to explore books, view detailed information, and ask
natural language questions powered by a Large Language Model.

------------------------------------------------------------------------

## Features

-   Scrape book data using Selenium\
-   Store data in Django backend\
-   Generate summaries using Transformers\
-   Semantic search using Sentence Transformers + ChromaDB\
-   AI Q&A using Gemini API\
-   Source citation support\
-   Book detail page with similar recommendations\
-   React-based frontend

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Django
-   Django REST Framework
-   Selenium
-   Sentence Transformers
-   ChromaDB
-   Gemini API

### Frontend

-   React
-   Axios
-   Tailwind CSS

------------------------------------------------------------------------

## Architecture

Scraper → Backend → Database → Embeddings → RAG → Gemini → Frontend

------------------------------------------------------------------------

## API Endpoints

### GET

-   /api/books/
-   /api/books/`<id>`{=html}/
-   /api/books/`<id>`{=html}/recommend/

### POST

-   /api/books/scrape/
-   /api/ask/

------------------------------------------------------------------------

## Setup

### Backend

cd backend python -m venv venv venv`\Scripts`{=tex}`\activate`{=tex} pip
install -r requirements.txt python manage.py migrate python manage.py
runserver

### Frontend

cd frontend npm install npm start

------------------------------------------------------------------------

## Environment Variables

GEMINI_API_KEY=your_key

------------------------------------------------------------------------

## Sample Questions

-   Which book has the highest rating?
-   Recommend a history book
-   What is Sapiens about?

------------------------------------------------------------------------

## Conclusion

This project demonstrates a complete AI-powered RAG system with
scraping, embeddings, and LLM integration.
