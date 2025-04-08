const defaultBackednURL = "http://0.0.0.0:8001"
export const  API_URL = (import.meta.env.VITE_BACKEND_URL ?? defaultBackednURL) + "/api/v1"
export const  BACKEND_SERVER_URL = import.meta.env.VITE_BACKEND_URL ?? defaultBackednURL
export const  SLACK_URL = "https://theailounge.slack.com"


