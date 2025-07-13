// src/components/ChoiceCard.jsx
export default function ChoiceCard({ idx, title, onSelect }) {
    return (
      <button
        onClick={onSelect}
        className="flex flex-col bg-white/90 rounded-xl shadow hover:shadow-lg transition p-4 w-full text-left"
      >
        <span className="text-sm text-gray-500 mb-1">Choix {idx + 1}</span>
        <span className="font-semibold">{title}</span>
      </button>
    );
  }