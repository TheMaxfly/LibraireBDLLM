// src/pages/Login.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();

  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(form.username, form.password);
      nav("/chat");
    } catch (err) {
      setError("Identifiants invalides");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-black/70 backdrop-blur-sm">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl p-8 shadow-xl w-80">
        <h1 className="text-2xl font-bold mb-6 text-center">Connexion</h1>
        <input
          name="username"
          placeholder="Nom d'utilisateur"
          className="border rounded w-full mb-4 p-2"
          value={form.username}
          onChange={handleChange}
        />
        <input
          name="password"
          type="password"
          placeholder="Mot de passe"
          className="border rounded w-full mb-4 p-2"
          value={form.password}
          onChange={handleChange}
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button className="w-full bg-amber-600 hover:bg-amber-700 text-white p-2 rounded">Se connecter</button>
      </form>
    </div>
  );
}