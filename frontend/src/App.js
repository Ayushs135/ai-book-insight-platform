import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import QA from "./pages/QA";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/qa" element={<QA />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;