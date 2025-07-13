// src/components/ChatBubble.jsx
export default function ChatBubble({ from, children }) {
    const me = from === "user";
    return (
      <div className={`flex ${me ? "justify-end" : "justify-start"} my-2`}>
        <div
          className={`max-w-[80%] p-3 rounded-2xl shadow-md whitespace-pre-line ${
            me ? "bg-amber-600 text-white" : "bg-white/90"
          }`}
        >
          {children}
        </div>
      </div>
    );
  }