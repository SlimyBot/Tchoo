<script setup>
import Lobby from "./Lobby.vue";
import MultiplesAnswers from "./MultiplesAnswers.vue";
import ErrorPage from "./ErrorPage.vue";
import ConnexionToSession from "./ConnexionToSession.vue";
import BetweenQuestions from "./BetweenQuestions.vue";
import StartSurvey from "../survey/StartSurvey.vue";

import { WEBSOCKET_BASE_URL } from "@/lib/baseURL";
import { ANSWER_MAP } from "@/lib/constants";
import { getToken } from "@/lib/auth";
import { io } from "socket.io-client";
import openStore from "@/lib/openAnswersStore";

import { ref } from "vue"
import { useRoute, useRouter } from "vue-router";

import "@/../node_modules/awesome-notifications/dist/style.css";
import AWN from "awesome-notifications";
import FreeAnswer from "./FreeAnswer.vue";
import TeacherScreen from "./TeacherScreen.vue";

const notifier = new AWN({ icons: { enabled: false, durations: { global: 1000 } } } )

const sessionState = ref("connecting")
let isOwner = false
const errorMsg = ref("")

const playerCount = ref(0)
const currentQuestion = ref({})
const currentQuestionType = ref("")
const currentAnswers = ref([])

function sessionError(message) {
  errorMsg.value = message
  sessionState.value = "error"
}

const router = useRouter()
const route = useRoute()
const joinCode = route.params.joinCode

const token = getToken()

const client = io(WEBSOCKET_BASE_URL, {
  path: "/ws",
  auth: token,
  transports: ["websocket"]
})

client.on("connect", () => {
  console.log("Connecté à la session")

  client.emit("session_connect", joinCode, (code, msg) => {
    console.log("Après session_connect : " + code + " : " + msg)

    if (["already_joined", "join_not_allowed", "not_joinable", "already_participated"].includes(code)) {
      sessionError(msg)

      // Si un utilisateur normal rejoind
    } else if (code === "join") {
      sessionState.value = "waiting"

      // Si le propriétaire de la session rejoind
    } else if (code === "owner_join") {
      sessionState.value = "owner_join"
      isOwner = true
    }
  })
})

client.on("user_answered", (email) => {
  console.log(email + " à répondu")

  if (!isOwner) return;
  notifier.success(email + " à répondu")
})

client.on("user_open_answered", (text) => {
  console.log("Réponse ouverte reçue : " + text)

  openStore.addOpenAnswer(text)
})

client.on("user_join", (email) => {
  console.log(email + " à rejoind")
  playerCount.value++

  if (!isOwner) return;
  notifier.info(email + " à rejoins")
})

client.on("user_leave", (email) => {
  console.log(email + " à quitté")
  playerCount.value--

  if (!isOwner) return;
  notifier.warning(email + " à quitté")
})

client.on("next_question", (data) => {
  console.log(data)
  currentQuestion.value = data.question
  currentQuestionType.value = data.type
  currentAnswers.value = data.answers

  openStore.clear()

  if (isOwner) {
    sessionState.value = "owner_next_question"
  } else if (data.type.includes("open")) { // Si question ouverte
    sessionState.value = "next_open_question"
  } else {
    sessionState.value = "next_question"
  }
})

/**
 * Apellé pour envoyer une réponse d'un utilisateur.
 */
function emitUserAnswer(clickedArrows) {
  let answers = [...currentAnswers.value]
  answers.sort((a, b) => a.id - b.id)

  let savedAnswers = []
  for (const [arrowButton, isClicked] of Object.entries(clickedArrows)) {
    if (isClicked) {
      let answerID = answers[ANSWER_MAP[arrowButton]].id
      savedAnswers.push(answerID)
    }
  }

  console.log("Envoi des réponses : " + savedAnswers)

  client.emit("user_answer", savedAnswers, (code, msg) => {
    console.log(code + " : " + msg)

    sessionState.value = "user_answer"
  })
}

/**
 * Apellé pour envoyer une réponse ouverte d'un utilisateur.
 */
function emitUserOpenAnswer(questionId, text) {
  console.log("Envoie réponse ouverte : " + text);

  client.emit("user_open_answer", questionId, text, (code, msg) => {
    console.log(code + " : " + msg)

    sessionState.value = "user_answer"
  })
}

function ownerShowResults(state) {
  console.log("show results " + state);
}

function ownerPauseAnswers(state) {
  console.log("pause answers " + state);
}

function innerWhenSessionEnd() {
  client.emit("end_session", (code, msg) => {
    console.log(code + " : " + msg)

    // La page de résultats s'affiche pour les propriétaire
    router.push("/endSurvey/" + joinCode)
  })
}

/**
 * Passage a la prochaine question pour le propriétaire.
 */
function ownerNextQuestion() {
  client.emit("initiate_next_question", (code, msg) => {
    console.log(code + " : " + msg)

    if (code === "no_more_questions") {
      innerWhenSessionEnd()
    }
  })
}

function ownerStopSession() {
  innerWhenSessionEnd()
}

client.on("session_end", (resultId) => {
  console.log("Notification de fin de session avec comme id de resultats : " + resultId)

  if (!isOwner) {
    router.push("/surveys") // TODO : changer quand séparation claire prof // étudiant
    return
  }
})

client.on("disconnect", () => {
  console.log("Déconnecté de la session")
  sessionError("Déconnecté de la session")
  client.disconnect()
})

client.on("connect_error", (msg) => {
  console.error("Refus de connexion :" + msg);
})
</script>

<template>
  <!-- Erreur pour rejoindre la session -->
  <ErrorPage
    v-if="sessionState === 'error'"
    :error-msg="errorMsg"
  />

  <!-- Connexions au sockets de la session -->
  <ConnexionToSession
    v-else-if="sessionState === 'connecting'"
    :code="joinCode"
  />

  <!-- Utilsateur : attente du démarage de la session -->
  <Lobby
    v-else-if="sessionState === 'waiting'"
    :code="joinCode"
  />

  <!-- Utilisateur : page de question qui s'affiche -->
  <MultiplesAnswers 
    v-else-if="sessionState === 'next_question'"
    :nb-answers="currentAnswers.length"
    @answer="(clickedArrows) => emitUserAnswer(clickedArrows)"
  />

  <!-- Utilisateur : page de question ouverte qui s'affiche -->
  <FreeAnswer
    v-else-if="sessionState === 'next_open_question'"
    :is-restricted="currentQuestionType === 'open_restricted'"
    @answer="(text) => emitUserOpenAnswer(currentQuestion.id, text)"
  />

  <!-- Utilisateur : réponse enregistrée -->
  <BetweenQuestions v-else-if="sessionState === 'user_answer'" />

  <!-- Propriétaire : écran pour démarrer -->
  <StartSurvey
    v-else-if="sessionState == 'owner_join'"
    :survey-name="joinCode"
    :player-count="playerCount"
    survey-time="&#8734;"
    @start-survey="ownerNextQuestion()"
  />

  <!-- Propriétaire : page de questions (qcm et ouverte) + controles de sessions -->
  <TeacherScreen
    v-else-if="sessionState === 'owner_next_question'"
    :question="currentQuestion"
    :question-type="currentQuestionType"
    :answers="currentAnswers"

    @show-results="ownerShowResults"
    @pause-answers="ownerPauseAnswers"
    @next-question="ownerNextQuestion()"
    @stop-session="ownerStopSession()"
  />

  <!-- Si il y a une faute de frappe dans sessionState (cette erreur ne devrai jamais apparaitre) -->
  <ErrorPage
    v-else
    :error-msg="'sessionState inconnu : ' + sessionState"
  />
</template>
