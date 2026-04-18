import { useEffect, useState } from "react";
import API from "../services/api";

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("books/")
      .then(res => setBooks(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="p-6">Loading books...</p>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">📚 Book Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {books.map(book => (
          <div
            key={book.id}
            className="bg-white p-4 rounded-2xl shadow-md hover:shadow-lg transition"
          >
            <h2 className="font-bold text-lg">{book.title}</h2>

            {book.author !== "Unknown" && (
              <p className="text-sm text-gray-500">{book.author}</p>
            )}

            <p className="mt-2 text-gray-700 text-sm line-clamp-3">
              {book.summary || book.description}
            </p>

            <div className="mt-3 flex items-center justify-between">
              <span className="text-yellow-500">⭐ {book.rating}</span>

              <a
                href={book.url}
                target="_blank"
                rel="noreferrer"
                className="text-blue-500 text-sm"
              >
                View
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}