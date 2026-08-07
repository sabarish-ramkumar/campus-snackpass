import axios from "axios";

// In dev, this falls back to your local FastAPI server.
// In production (Vercel), set VITE_API_URL to your deployed Render backend URL.
const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = axios.create({ baseURL });

export default client;
