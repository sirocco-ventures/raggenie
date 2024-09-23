const defaultBackednURL = "http://localhost:8080"
export const  API_URL = (import.meta.env.VITE_BACKEND_URL ?? defaultBackednURL) + "/api/v1"
export const  BACKEND_SERVER_URL = import.meta.env.VITE_BACKEND_URL ?? defaultBackednURL


