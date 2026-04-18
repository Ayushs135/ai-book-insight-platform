import { useState } from "react";
import API from "../services/api";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);
    try {
      const res = await API.post("ask/", { question });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("Error fetching answer");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold">Ask AI</h1>

      <input
        className="border p-2 w-full mt-4 rounded"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about books..."
      />

      <button
        onClick={askQuestion}
        className="bg-blue-500 text-white px-4 py-2 mt-4 rounded"
      >
        Ask
      </button>

      {loading && <p className="mt-4">Thinking...</p>}

      {answer && (
        <div className="mt-4 p-4 border rounded bg-white">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}