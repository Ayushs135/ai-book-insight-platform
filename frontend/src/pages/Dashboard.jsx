import { useEffect, useState } from "react";
import { Link } from "react-router-dom";  
import API from "../services/api";

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBooks = () => {
    API.get("books/")
      .then(res => setBooks(res.data))
      .finally(() => setLoading(false));
  };

  const scrapeBooks = async () => {
    setLoading(true);
    await API.post("books/scrape/");
    fetchBooks();
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  if (loading) {
    return <p className="text-center mt-10">Loading books...</p>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      
      {/* Header */}
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">📚 Book Insights</h1>

          <button
            onClick={scrapeBooks}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
          >
            Scrape Books
          </button>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {books.map(book => (
            <div
              key={book.id}
              className="bg-white p-5 rounded-2xl shadow hover:shadow-lg transition duration-300"
            >
              
              {}
              <h2 className="font-semibold text-lg">
                <Link
                  to={`/book/${book.id}`}
                  className="hover:underline text-blue-600"
                >
                  {book.title}
                </Link>
              </h2>

              <p className="text-sm text-gray-500">
                Author: {book.author}
              </p>

              <p className="mt-2 text-gray-700 text-sm line-clamp-3">
                {book.summary || book.description}
              </p>

              <div className="flex justify-between items-center mt-4">
                <span className="text-yellow-500 font-medium">
                  ⭐ {book.rating}
                </span>

                <a
                  href={book.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-500 text-sm"
                >
                  View →
                </a>
              </div>
            </div>
          ))}

        </div>
      </div>
    </div>
  );
}