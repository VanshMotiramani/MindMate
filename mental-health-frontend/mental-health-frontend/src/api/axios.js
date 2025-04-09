import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // This header bypasses ngrok's browser warning
    'ngrok-skip-browser-warning': 'true',
  },
});

export default api;
