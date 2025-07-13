// src/hooks/useAuth.js
import { useState } from "react";
import api, { setAuthToken } from "../api";
import jwtDecode from "jwt-decode";

export default function useAuth() {
  const [user, setUser] = useState(() => {
    const t = localStorage.getItem("token");
    if (!t) return null;
    setAuthToken(t);
    return jwtDecode(t);
  });

  async function login(username, password) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);
    const { data } = await api.post("/token", params);
    localStorage.setItem("token", data.access_token);
    setAuthToken(data.access_token);
    setUser(jwtDecode(data.access_token));
  }

  function logout() {
    localStorage.removeItem("token");
    setAuthToken(null);
    setUser(null);
  }

  return { user, login, logout };
}