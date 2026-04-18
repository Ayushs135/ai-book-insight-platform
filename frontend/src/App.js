import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import BookDetail from "./pages/BookDetail";
import QA from "./pages/QA";

// Navbar Component
function Navbar() {
  return (
    <div className="bg-white shadow p-4 flex justify-between">
      <h1 className="font-bold text-lg">AI Book Platform</h1>

      <div className="flex gap-4">
        <Link to="/" className="hover:underline">
          Dashboard
        </Link>
        <Link to="/qa" className="hover:underline">
          Ask AI
        </Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        {/* Dashboard */}
        <Route path="/" element={<Dashboard />} />

        {/* Book Detail Page */}
        <Route path="/book/:id" element={<BookDetail />} />

        {/* Q&A Page */}
        <Route path="/qa" element={<QA />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;