// src/pages/Chat.jsx
import { useState } from "react";
import api from "../api";
import ChatBubble from "../components/ChatBubble";
import ChoiceCard from "../components/ChoiceCard";

export default function Chat() {
  const [prompt, setPrompt] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendPrompt() {
    if (!prompt.trim()) return;
    setHistory((h) => [...h, { from: "user", text: prompt }]);
    setPrompt("");
    setLoading(true);
    try {
      const { data } = await api.post("/recommend", { prompt });
      // découper la réponse en bullet points en se basant sur les sauts de ligne
      const lines = data.recommendation.split(/\n+/).filter((l) => l.trim());
      const titleLines = lines.filter((l) => l.startsWith("1") || l.startsWith("2") || l.startsWith("3"));

      setHistory((h) => [
        ...h,
        {
          from: "bot",
          text: data.recommendation,
          titles: titleLines.map((line) => line.replace(/^\d+\.\s*/, "")),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center pt-10 pb-24 min-h-screen bg-black/60 backdrop-blur">
      <div className="w-full max-w-2xl bg-white/70 rounded-3xl shadow-xl p-6">
        <div className="h-[60vh] overflow-y-auto pr-2">
          {history.map((msg, i) => (
            <div key={i}>
              <ChatBubble from={msg.from}>{msg.text}</ChatBubble>
              {msg.titles && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-2">
                  {msg.titles.map((t, idx) => (
                    <ChoiceCard key={idx} idx={idx} title={t} onSelect={() => alert(t)} />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-4 flex gap-2">
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendPrompt()}
            className="flex-1 border rounded-xl p-3"
            placeholder="Pose ta question…"
          />
          <button
            disabled={loading}
            onClick={sendPrompt}
            className="bg-amber-600 hover:bg-amber-700 text-white px-4 rounded-xl disabled:opacity-50"
          >
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}