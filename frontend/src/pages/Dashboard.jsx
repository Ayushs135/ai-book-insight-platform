import { useEffect, useState } from "react";
import API from "../services/api";

export default function Dashboard() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    API.get("books/")
      .then(res => setBooks(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Books</h1>

      <div className="grid grid-cols-3 gap-4">
        {books.map(book => (
          <div key={book.id} className="border p-4 rounded shadow">
            <h2 className="font-bold">{book.title}</h2>
            <p className="text-sm">{book.author}</p>
            <p className="text-yellow-500">⭐ {book.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
}