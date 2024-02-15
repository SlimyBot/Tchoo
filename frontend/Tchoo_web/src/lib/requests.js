import { getAuthHeader } from "./auth.js";
import { BASE_URL } from "./baseURL.js";

function checkShouldRedirect(statusCode) {
  if (statusCode === 403 || statusCode === 401) {
    console.warn(`Code http ${statusCode} reçus.`)
    console.warn("Cela signifie que soit l'utilisateur est déconécté, soit il n'a pas le droit de faire ce qu'il a fait.")
    console.warn("Redirection automatique vers /casLogin...")

    window.location.href = "/casLogin";
  }
}

/**
 * GET une requête retournant du JSON à l'api avec authentification.
 * @param {string} url L'url de l'api.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
async function getJsonAuth(url) {
  const res = await window.fetch(url, {
    headers: getAuthHeader(),
    method: "GET",
  });

  checkShouldRedirect(res.status);

  return [await res.json(), res.status];
}

async function requestWithBody(url, data, method) {
  const res = await window.fetch(url, {
    headers: {
      ...{ "Content-Type": "application/json" },
      ...getAuthHeader(),
    },
    method: method,
    body: JSON.stringify(data),
  });

  checkShouldRedirect(res.status);

  return [await res.json(), res.status];
}

/**
 * POST une requête JSON à l'api avec authentification.
 * @param {string} url L'url de l'api.
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
async function postJsonAuth(url, data) {
  return await requestWithBody(url, data, "POST");
}

/**
 * POST une requête JSON à l'api sans authentification.
 * @param {string} url L'url de l'api.
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
async function postJson(url, data) {
  const res = await window.fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return [await res.json(), res.status];
}


/**
 * PUT une requête JSON à l'api avec authentification.
 * @param {string} url L'url de l'api.
 * @param {string} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
async function putJsonAuth(url, data) {
  return await requestWithBody(url, data, "PUT");
}


export async function register(name, surname, email, affiliation) {
  return await postJson(`${BASE_URL}/users/register`, {
    name,
    surname,
    email,
    affiliation
  });
}


/**
 * DELETE une requête JSON à l'api avec authentification.
 * @param {string} url L'url de l'api.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
async function deleteJsonAuth(url) {
  const res = await window.fetch(url, {
    headers: {
      ...{ "Content-Type": "application/json" },
      ...getAuthHeader(),
    },
    method: "DELETE",
  });

  return [await res.json(), res.status];
}

/**
 * Récupère les informations de l'utilisateur connecté.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
export async function fetchUserInfo() {
  return await getJsonAuth(`${BASE_URL}/users/me`);
}

/**
 * Modifie les informations de l'utilisateur connecté.
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
export async function modifyUserInfo(data) {
  return await postJsonAuth(`${BASE_URL}/users/me`, data);
}

/**
 * Concerne les questions et les questionnaires. 
 */

/**
 * Créer un questionnaire dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function createSurvey(title, subject) {
  return await postJsonAuth(`${BASE_URL}/question/create_survey`, {
    title,
    subject
  });
}

/**
 * Récupère les questionnaires d'un utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'api et le code de statut de la requête.
 */
export async function getSurveys() {
    return await getJsonAuth(`${BASE_URL}/question/read_surveys`);
}

/**
 * Récupère les informations d'un questionnaire à partir de l'identifiant du questionnaire passé en paramètre.
 * @param {number} surveyId L'identifiant du questionnaire.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getSurveyInfo(surveyId) {
  return await getJsonAuth(`${BASE_URL}/question/get_survey_info/${surveyId}`);
}

/**
 * Récupère les questions qui compose le questionnaire à partir de l'identifiant de questionnaire passé en paramètre.
 * @param {number} surveyId L'identifiant de la question.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getSurvey(surveyId) {
  return await getJsonAuth(`${BASE_URL}/question/read_survey/${surveyId}`); 
}

/* TODO a check survey = title + subject*/
/**
 * Met à jour un questionnaire dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function updateSurvey(survey_id, title, subject) {
  return await putJsonAuth(`${BASE_URL}/question/update_survey`, {
    survey_id,
    title,
    subject,
  });
}

/**
 * Supprime un questionnaire dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function deleteSurvey(survey_id) {
  return await deleteJsonAuth(`${BASE_URL}/question/delete_survey?survey_id=${survey_id}`);
}

/**
 * Créer une question dans la base de données.
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function createQuestion(type, text, media) {
  return await postJsonAuth(`${BASE_URL}/question/create_question`, {
    type,
    text,
    media
  });
}

/**
 * Récupère les questions de utilisateur connecté pour sa banque de question.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getQuestionsBank() {
  return await getJsonAuth(`${BASE_URL}/question/read_questions_bank`);
}

/**
 * Récupère une question et ses réponses à partir de l'identifiant de la question.
 * @param {number} questionId 
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getQuestion(questionId) {
  return await getJsonAuth(`${BASE_URL}/question/read_question/${questionId}`); 
}


/**
 * Récupère les groupes de l'utilisateur connecté.	
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getAllGroups() {
  return await getJsonAuth(`${BASE_URL}/groups/get_groups`);
}

/**
 * Récupère un utilisateur à partir de son identifiant.
 * @param {number} userId L'identifiant de l'utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getUser(userId) {
  return await getJsonAuth(`${BASE_URL}/users/get_user/${userId}`);
}

/**
 * Récupère un utilisateur à partir de son adresse email.
 * @param {string} userEmail L'adresse email de l'utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getUserByEmail(userEmail) {
  return await getJsonAuth(`${BASE_URL}/users/get_user_by_email/${userEmail}`);
}


/**
 * Récupère les utilisateurs d'un groupe à partir de l'identifiant du groupe.
 * @param {number} groupId L'identifiant du groupe.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getUsersFromGroup(groupId) {
  return await getJsonAuth(`${BASE_URL}/groups/get_group_users/${groupId}`);
}
/**
 * Récupère les informations d'un groupe à partir de l'identifiant du groupe.
 * @param {number} groupId L'identifiant du groupe.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getGroup(groupId) {
  return await getJsonAuth(`${BASE_URL}/groups/${groupId}`);
}

/**
 * Créer un groupe à partir du nom du groupe et de l'id du groupe parent.
 * @param {string} name Le nom du groupe.
 * @param {$Ref} parent Le groupe parent.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function createGroup(name, parent) {
  let url = `${BASE_URL}/groups/create_group?group_name=${name}`;
  if (parent !== undefined && parent !== '' && parent !== null ) {
    url += `&parent_group_id=${parent}`;
  }

  return await postJsonAuth(url, {}); // Assuming postJsonAuth(url, data) sends a POST request with data in the request body
}
/**
* Met à jour une question dans la base de données.                                           
* @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
* @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
*/
export async function updateQuestion(question_id, text, media, type){
 return await putJsonAuth(`${BASE_URL}/question/update_question`, {
   question_id,
   text,
   media,
   type
  });
}

/**
 * Supprime un groupe à partir de l'identifiant du groupe.
 * @param {number} groupId L'identifiant du groupe.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function deleteGroup(groupId) {
  return await deleteJsonAuth(`${BASE_URL}/groups/delete_group/${groupId}`);
}

/**
 * Modifier un groupe à partir de l'identifiant du groupe et du nouveau nom du groupe.
 * @param {number} groupId L'identifiant du groupe.
 * @param {string} name Le nouveau nom du groupe.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function updateGroup(groupId, name) {
  return await putJsonAuth(`${BASE_URL}/groups/update_group/${groupId}?name=${name}`, {});
}


/**
 *  * Supprime une question de la base de données définitivement (supprime aussi ses liens aux questionnaires et ses réponses).
 * il faut demander la confirmation de l'utilisateur avant de supprimer une question.
 * @param {number} questionId 
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function removeQuestion(questionId) {
  return await deleteJsonAuth(`${BASE_URL}/question/delete_question?id_question=${questionId}`);
}

/**
 * Fait le lien entre un questionnaire et une question dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function linkQuestion(question_id, survey_id) {
  return await postJsonAuth(`${BASE_URL}/question/link_question?question_id=${question_id}&survey_id=${survey_id}`);
}

/**
 * Supprime le lien entre un questionnaire et une question dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function unlinkQuestion(question_id, survey_id) {
  return await deleteJsonAuth(`${BASE_URL}/question/unlink_question?survey_id=${survey_id}&question_id=${question_id}`);
}

/**
 * Créer un questionnaire dans la base de données.                                           
 * @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function createAnswer(question_id, text, is_good_answer){
  return await postJsonAuth(`${BASE_URL}/question/create_answer`, {
    question_id,
    text,
    is_good_answer,
  });
}

/**
 * Ajoute un utilisateur à un groupe à partir de l'identifiant du groupe et de l'identifiant de l'utilisateur.
 * @param {number} groupId L'identifiant du groupe.
 * @param {number} userId L'identifiant de l'utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function addUserToGroup(groupId, userId) {
  return await postJsonAuth(
    `${BASE_URL}/groups/add_member/${groupId}?member_id=${userId}`);
}

/**
 * Supprime un utilisateur d'un groupe à partir de l'identifiant du groupe et de l'identifiant de l'utilisateur.
 * @param {number} groupId L'identifiant du groupe.
 * @param {number} userId L'identifiant de l'utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function removeUserFromGroup(groupId, userId) {
  return await deleteJsonAuth(
    `${BASE_URL}/groups/remove_member/${groupId}?member_id=${userId}`);
}

/**
* modifie un questionnaire dans la base de données.                                           
* @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
* @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
*/
export async function updateAnswer(id_answer, text, is_good_answer){
  return await putJsonAuth(`${BASE_URL}/question/update_answer`, {
    id_answer,
    text,
    is_good_answer
  });
}

/**
* supprimer un questionnaire dans la base de données.                                           
* @param {object} data Les données à envoyer à l'api sous la forme d'un objet javascript.
* @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
*/
export async function deleteAnswer(answer_id){
  return await deleteJsonAuth(`${BASE_URL}/question/delete_answer?answer_id=${answer_id}`);
}

/**
 * Renvoie la liste des modèles des sessions de questionaires
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getAllSessionTemplates() {
  return await getJsonAuth(`${BASE_URL}/sessions/template/all`);
}

/**
 * Renvoie un modèle de session.
 * @param {number} sessionTemplateId L'identifiant du modèle de session
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getSessionTemplate(sessionTemplateId) {
  return await getJsonAuth(`${BASE_URL}/sessions/template/${sessionTemplateId}`);
}

/**
 * Créer un nouveau modèle de session de questionaire.
 * @param {number} surveyId L'ID du questionaire à lier a ce modèle.
 * @param {string} name Le nom du modèle.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function createSessionTemplate(surveyId, name) {
  return await postJsonAuth(`${BASE_URL}/sessions/template/new`, {
    survey_id: surveyId,
    name: name,
  });
}

/**
 * Modifie un modèle de session.
 * @param {number} sessionTemplateId L'ID du modèle de session.
 * @param {number} surveyId L'ID du questionaire attaché.
 * @param {string} name Le nom du modèle.
 * @param {('piloted'|'auto_timer'|'auto_free')} type Le type de session.
 * @param {boolean} isPublic Si la session est publique ou non.
 * @param {boolean} showAnswers Si on affiche les réponses à la fin de chaque questions.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function updateSessionTemplate(sessionTemplateId, surveyId, name, type, authorisedGroupId, showAnswers) {
  return await putJsonAuth(`${BASE_URL}/sessions/template/update/${sessionTemplateId}`, {
    name: name,
    type: type,
    authorised_group_id: authorisedGroupId,
    show_answers: showAnswers,
    survey_id: surveyId
  });
}

/**
 * Supprime un modèle de session de questionaire.
 * @param {number} sessionTemplateId L'ID du modèle de session.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function deleteSessionTemplate(sessionTemplateId) {
  return await deleteJsonAuth(`${BASE_URL}/sessions/template/delete/${sessionTemplateId}`);
}

/**
 * Créer et démare une session de questionaire.
 * @param {number} sessionTemplateId Le modèle de session depuis lequel il faut démarer la session.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function startSurveySession(sessionTemplateId) {
  return await postJsonAuth(`${BASE_URL}/sessions/start`, {session_template_id: sessionTemplateId});
}

/**
 * Renvoie la liste de toutes les sessions de questionaire lancées par l'utilisateur.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getAllSurveySessions() {
  return await getJsonAuth(`${BASE_URL}/sessions/all`);
}

/**
 * Récupère le résultat des 3 premiers joueurs du code d'une session.
 * @param {str} join_code Code de la session.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getEndSurvey(join_code) {
  return await getJsonAuth(`${BASE_URL}/endSurvey/get_end_survey/${join_code}`);
}

/**
 * Récupère le résultat de tous les joueurs du coded d'une session.
 * @param {str} id_player L'identifiant de l'utilisateur.
 * @param {str} join_code Code de la session.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getPlayerDetails(id_player, join_code) {
  return await getJsonAuth(`${BASE_URL}/endSurvey/get_player_details/${id_player}/${join_code}`);
}

/**
 * Récupère les sessions auxquelles le joueur a participé.
 * @returns {[object, number]} Un tableau contenant la réponse de l'API et le code de statut de la requête.
 */
export async function getSessionsPlayer() {
  return await getJsonAuth(`${BASE_URL}/results/get_sessions_player`);
}
