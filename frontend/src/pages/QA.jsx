import { useState } from "react";
import API from "../services/api";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    const res = await API.post("ask/", { question });
    setAnswer(res.data.answer);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Ask AI</h1>

      <input
        className="border p-2 w-full mt-4"
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

      {answer && (
        <div className="mt-4 p-4 border rounded">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}