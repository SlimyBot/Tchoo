// URL de base de l'API
export const BASE_URL = import.meta.env.PROD ? "/api" : "//localhost:8000/api";

// URL de base des websockets
export const WEBSOCKET_BASE_URL = import.meta.env.PROD ? "/session" : "localhost:8000/session";

//URL du CAS
export const CAS_URL = "https://localhost:8443";

// URL de service pour le CAS
export const CAS_SERVICE_URL = "http://localhost:5173";