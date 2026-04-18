import { useState } from "react";
import API from "../services/api";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;

    const newMessages = [...messages, { type: "user", text: question }];
    setMessages(newMessages);
    setQuestion("");
    setLoading(true);

    try {
      const res = await API.post("ask/", { question });

      setMessages([
        ...newMessages,
        {
          type: "bot",
          text: res.data.answer,
          sources: res.data.sources || []   // store sources
        }
      ]);
    } catch {
      setMessages([
        ...newMessages,
        { type: "bot", text: "Error getting response", sources: [] }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* Header */}
      <div className="p-4 bg-white shadow text-lg font-semibold">
        🤖 Ask AI
      </div>

      {/* Chat */}
      <div className="flex-1 p-6 max-w-3xl mx-auto w-full">

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-4 p-3 rounded-lg max-w-xl ${
              msg.type === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-white shadow"
            }`}
          >
            {/* Message text */}
            <p>{msg.text}</p>

            {/* Sources (only for bot) */}
            {msg.type === "bot" && msg.sources && msg.sources.length > 0 && (
              <div className="mt-3 text-sm text-gray-500">
                <strong>Sources:</strong>
                {msg.sources.map((s) => (
                  <p key={s.id} className="text-blue-500 hover:underline cursor-pointer">
                    {s.title}
                  </p>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && <p className="text-gray-500">Thinking...</p>}

      </div>

      {/* Input */}
      <div className="p-4 bg-white flex gap-2">
        <input
          className="flex-1 border p-2 rounded"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about books..."
        />

        <button
          onClick={askQuestion}
          className="bg-blue-500 text-white px-4 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}