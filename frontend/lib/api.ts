// frontend/lib/api.ts

const BACKEND_PROD_URL = "https://celestial-biome-app-617827263662.asia-northeast1.run.app";

export const API_BASE_URL =
  typeof window !== "undefined" &&
  (window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1")
    ? "http://localhost:8000" // ローカルで Next dev ＋ Django 用
    : BACKEND_PROD_URL;
