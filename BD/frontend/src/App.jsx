import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.post(
      "http://localhost:8000/recommend",
      { prompt },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setAnswer(res.data.response);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <textarea
        className="w-full border rounded p-2"
        rows={4}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        className="mt-2 bg-blue-600 text-white px-4 py-2 rounded"
        onClick={ask}
      >
        Demander une reco
      </button>
      <pre className="mt-4 whitespace-pre-wrap">{answer}</pre>
    </div>
  );
}

export default App;
