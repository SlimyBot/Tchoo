import jwt_decode from "jwt-decode";

/**
 * Sauvegarde le token JWT dans le localStorage
 * @param {string} token
 */
export function saveToken(token) {
  localStorage.setItem("jwt_token", token);
}

export function getToken() {
  return localStorage.getItem("jwt_token");
}

/**
 * Renvoie les entêtes d'authentification pour faire un appel à l'api qui
 * nécessite d'être authentifié.
 */
export function getAuthHeader() {
  return {
    Authorization: `Bearer ${localStorage.getItem("jwt_token")}`,
  };
}

/**
 * Verifie la session de connexion de l'utilisateur est valide.
 * @returns {boolean} true si l'utilisateur est connecté, false sinon.
 */
export function isLoggedIn() {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    return false;
  }

  // est-ce que la session est expirée ?
  const decoded = jwt_decode(token);

  if (decoded.exp < Date.now() / 1000) {
    return false;
  } else {
    return true;
  }
}

/**
 * Verifie si l'utilisateur est un professeur.
 * @returns {boolean} true si l'utilisateur est un professeur, false sinon.
 */
export function isTeacher() {
  const token = localStorage.getItem("jwt_token");
  const decoded = jwt_decode(token);

  return decoded.aff === "teacher";
}

/**
 * Supprime le token JWT du localStorage, déconnectant l'utilisateur.
 */
export function logout() {
  localStorage.removeItem("jwt_token");
}
