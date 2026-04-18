import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import QA from "./pages/QA";

function Navbar() {
  return (
    <div className="bg-white shadow p-4 flex justify-between">
      <h1 className="font-bold">AI Book Platform</h1>

      <div className="flex gap-4">
        <Link to="/">Dashboard</Link>
        <Link to="/qa">Ask AI</Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/qa" element={<QA />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;