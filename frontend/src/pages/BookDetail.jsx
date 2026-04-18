import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../services/api";

export default function BookDetail() {
  const { id } = useParams();

  const [book, setBook] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const bookRes = await API.get(`books/${id}/`);
        setBook(bookRes.data);

        const simRes = await API.get(`books/${id}/recommend/`);
        setSimilar(simRes.data);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };

    fetchData();
  }, [id]);

  if (loading) return <p className="p-6">Loading...</p>;
  if (!book) return <p className="p-6">Book not found</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow">

        {/* Title */}
        <h1 className="text-2xl font-bold">{book.title}</h1>

        {/* Author */}
        <p className="text-gray-500 mt-1">
          Author: {book.author}
        </p>

        {/* Rating */}
        <p className="text-yellow-500 mt-2">
          ⭐ {book.rating}
        </p>

        {/* Description */}
        <p className="mt-4 text-gray-700">
          {book.description}
        </p>

        {/* Summary */}
        <div className="mt-4 p-4 bg-blue-50 rounded">
          <strong>Summary:</strong>
          <p>{book.summary}</p>
        </div>

        {/* URL */}
        <a
          href={book.url}
          target="_blank"
          rel="noreferrer"
          className="text-blue-500 mt-4 inline-block"
        >
          View Original →
        </a>

      </div>

      {/* Similar Books */}
      <div className="max-w-4xl mx-auto mt-8">
        <h2 className="text-xl font-bold mb-4">
          📚 Similar Books
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          {similar.map((b) => (
            <div
              key={b.id}
              className="bg-white p-4 rounded shadow hover:shadow-lg"
            >
              <h3 className="font-semibold">
                <Link to={`/book/${b.id}`} className="hover:underline">
                  {b.title}
                </Link>
              </h3>

              <p className="text-sm text-gray-500">
                {b.author}
              </p>

              <p className="text-yellow-500 text-sm">
                ⭐ {b.rating}
              </p>
            </div>
          ))}

        </div>
      </div>
    </div>
  );
}