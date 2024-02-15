<script setup>

import Gear from "@/components/Gear.vue";
import ClearButton from "@/components/ClearButton.vue";
import Header from '@/components/Header.vue';
import ClearButtonSelector from "@/components/ClearButtonSelector.vue";
import ButtonPublicPrivate from "@/components/pages/survey/ButtonPublicPrivate.vue";
import ImportSurvey from "../survey/ImportSurvey.vue";
import { useRouter } from "vue-router";

const router = useRouter();
import { ref, provide, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getSessionTemplate, updateSessionTemplate, getSurveyInfo, startSurveySession, getAllGroups } from "@/lib/requests"

const route = useRoute();
const templateID = route.params.id

const showImportSurvey = ref(false)

const choosenSurveyData = ref({})

const selectedAccess = ref("public");
const sessionType = ref("")

const showAnswers = ref(false)
const annonAnswers = ref(false)

const template = ref(null)
provide("template", template)

const selectedGroupId = ref(null)
const allGroups = ref([])

onMounted(async () => {
  const [json, code] = await getSessionTemplate(templateID)

  if (code !== 200) {
    console.error(json)
    return;
  }

  template.value = json

  sessionType.value = template.value.type
  showAnswers.value = template.value.showAnswers
  selectedAccess.value = template.value.authorised_group_id === null ? "public" : "private"
  if (selectedAccess.value === "private") {
    selectedGroupId.value = template.value.authorised_group_id
  }

  await refreshSurveyData()

  // Get groups
  const [gJson, gCode] = await getAllGroups()

  if (gCode !== 200) {
    console.error(gJson)
    return
  }

  allGroups.value = gJson
})

async function updateTemplate() {
  const groupId = selectedAccess.value === 'public' ? null : selectedGroupId.value

  await updateSessionTemplate(
    templateID,
    template.value.survey_id,
    template.value.name,
    sessionType.value,
    groupId,
    showAnswers.value
  )
}

async function onSurveyChoosed() {
  showImportSurvey.value = false

  // Refresh survey
  await refreshSurveyData()
}

async function refreshSurveyData() {
  const [json, code] = await getSurveyInfo(template.value.survey_id)

  if (code !== 200) {
    console.error(json)
    return;
  }

  choosenSurveyData.value = json
}

async function startSurveySessionFromTemplate() {
  const [json, _] = await startSurveySession(templateID);
  const joinCode = json["join_code"];

  console.log("Session lancée depuis un modèle : " + joinCode);
  router.push("/session/" + joinCode);
}
</script>

<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  
  <body v-if="template">
    <Header />
    <div class="return">
      <button class="btnReturn">
        <img
          src="@/components/icons/return.svg"
          alt="return"
          @click="router.push('/AllSessions')"
        >
      </button>
    </div>
    <div class="top">
      <input
        v-model="template.name"
        class="SessionName"
        type="text"
        maxlength="25"
        :placeholder="$t('createSession.creaName')"
      >
    </div>
    <div class="buttonsList">
      <label>
        <input
          v-model="sessionType"
          type="radio"
          name="sessionType"
          value="piloted"
        >
        <span> 
          {{ $t("createSession.piloted") }}
          <!-- Session pilotée  -->
        </span>
      </label>
      <label>
        <input v-model="sessionType"
               type="radio"
               name="sessionType"
               value="auto_timer"
        >
        <span> 
          {{ $t("createSession.autoTime") }}
          <!-- Session automatique (minutée)  -->
        </span>
      </label>
      <label>
        <input v-model="sessionType"
               type="radio"
               name="sessionType"
               value="auto_free"
        >
        <span> 
          {{ $t("createSession.autoFree") }}
          <!-- Session automatique (libre)  -->
        </span>
      </label>

      <div class="QuizzList">
        <div v-if="showImportSurvey"
             class="import-survey-wrapper"
        >
          <p>
            {{ $t("createSession.importSurvey") }}
            <!-- Importer un questionaire -->
          </p>

          <ImportSurvey @survey-choosed="onSurveyChoosed" />
        </div>

        <div v-else
             class="imported-survey"
        >
          <p> 
            {{ $t("createSession.surveyLinked") }}
            <!-- Questionaire lié  -->
          </p>
          <div class="suvey-and-button">
            <div class="addSurvey">
              <h3 class="title">
                {{ choosenSurveyData.title }}
              </h3>
              <p>{{ $t ("survey.subject") }}  : {{ choosenSurveyData.subject }}</p>
            </div>

            <button class="switch-survey"
                    @click="showImportSurvey = true"
            >
              {{ $t("createSession.changeSurvey")  }}
              <!-- Changer de questionaire -->
            </button>
          </div>
        </div>
      </div>

      <hr>

      <div class="SessionDetails">
        <p> 
          {{ $t("createSession.sessionDetails")  }}
          <!-- Détails de la session  -->
        </p>
        <div class="Access">
          <i> 
            {{ $t("createSession.access")  }}
            <!-- Accessibilité :  -->
          </i>
          <select v-model="selectedAccess"
                  class="multiple"
          >
            <option value="public"
                    selected="selected"
            >
              {{ $t("createSession.public")   }}
              <!-- Public -->
            </option>
            <option value="private">
              {{ $t("createSession.private")  }}
              <!-- Privée -->
            </option>
          </select>

          <div v-if="selectedAccess === 'private'"
               style="display: inline-block"
          >
            <select
              v-model="selectedGroupId"
              class="multiple"
            >
              <option
                disabled
                value="null"
              >
                -- 
                {{ $t("createSession.selectGroup")   }}
                <!-- choisir un groupe  -->
                --
              </option>
              <option
                v-for="group of allGroups"
                :key="group.id"
                :value="group.id"
              >
                {{ group.group_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="AnswersVisibility">
          <i> 
            {{ $t("createSession.answersVisibility")   }}
            <!-- Affichage des réponses entre chaque question--> :
          </i>
          <label>
            <input v-model="showAnswers"
                   type="checkbox"
            >
            <span> 
              {{ $t("createSession.yes")  }}
              <!-- Oui  -->
            </span>
          </label>
        </div>

        <div class="Anonymous">
          <i> 
            {{ $t("createSession.anonymousAnswers")  }}
            <!-- Réponses anonymes:  -->
          </i>
          <label>
            <input v-model="annonAnswers"
                   type="checkbox"
            >
            <span> 
              {{ $t("createSession.yes")  }}
              <!-- Oui  -->
            </span>
          </label>
        </div>
        <div class="endPart">
          <div class="buttons">
            <button @click="updateTemplate()">
              {{ $t("createSession.save")   }}
              <!-- Sauvegarder -->
            </button>

            <button class="start"
                    @click="startSurveySessionFromTemplate()"
            >
              {{ $t("createSession.start")   }}
              <!-- Lancer la session -->
            </button>
          </div>
        </div>
      </div>
    </div>
    <Gear />
  </body>


  <body v-else>
    <div class="loader-container">
      <span class="loader" />
    </div>
  </body> 
</template>

<style scoped>
.loader-container {
  display: flex;
  align-content: center;
  justify-content: center;
}

.loader {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: inline-block;
  border-top: 3px solid var(--main-color);
  border-right: 3px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

body {
  height: 96vh;
  width: 98vw;
  color: var(--text-color);
}

.top {
  text-align: center;
  display: block;
}

input[type="radio"] {
  display: none;
}

input[type="radio"]:checked ~ span {
  background-color: var(--main-color);
  color: var(--white);
}

input[type="checkbox"] {
  display: none;
}

input[type="checkbox"]:checked ~ span {
  background-color: var(--main-color);
  color: var(--white);
}

label span {
  border: var(--main-color) 1px solid;
  font-size: 15px;
  font-family: "Sofia Sans", sans-serif;
  color: var(--main-color);
  padding: 12px;
  border-radius: 30px;
  margin-right: 20px;
  cursor: pointer;
}

.buttonsList {
  display: block;
  text-align: center;
  margin: 40px;
}

.SessionName {
  text-align: center;
  font-size: 30px;
  border: 0;
  text-decoration: var(--text-color) underline;
  text-underline-offset: 6px;
  background-color: transparent;
  color: var(--text-color);
}

.SessionName:focus-visible {
  outline: none;
}

.QuizzList {
  display: block;
  margin: 40px;

  font-family: "Sofia Sans", sans-serif;
  text-align: left;
}

.addSurvey {
  display: inline-block;
  background-color: var(--white);
  border-radius: 10px;
  border: var(--main-color) 1px solid;
  padding: 20px 40px;

  width : 200px;
  text-align: center;
}

.suvey-and-button {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 2em;
}

.switch-survey {
  background-color: var(--white);
  border-radius: 90px;
  border: var(--main-color) 1px solid;
  padding: 10px;
  cursor: pointer;
  color: var(--text-color);
}

.SessionDetails {
  display: block;
  margin: 40px;

  font-family: "Sofia Sans", sans-serif;
  text-align: left;
}

.buttons {
  display: flex;
  gap: 1em;
}

.buttons button {
  display: block;
  background-color: var(--white);
  border-radius: 90px;
  border: var(--main-color) 1px solid;
  padding: 10px;
  margin-left: auto;
  margin-right: auto;

  width: 30vw;
  text-align: center;
  color: var(--text-color);
  font-size: 20px;


  cursor: pointer;
  transition: linear 0.3s;
}

button:hover {
  background-color: var(--main-color);
  color: var(--white);
  transition: linear 0.3s;
}

.multiple {
  display: inline-block;
  background-color: var(--white);
  border-radius: 10px;
  border: var(--main-color) 1px solid;
  padding: 10px;

  width: 20vw;
  text-align: center;
  color: var(--text-color);

  cursor: pointer;
  margin-right: 20px;
}

.endPart {
  display: block;
  margin: 40px;

  font-family: "Sofia Sans", sans-serif;
  text-align: center;

}

i {
  display: inline-block;
  margin: 20px;
}

.return {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  margin: 0 0 1% 2%;
}

.btnReturn {
  background-color: transparent;
  border: none;
  border-radius: 100%;
  cursor: pointer;
  transition: 500ms;
  filter: var(--filter);
}

.btnReturn:hover {
  background-color: #17273a23;
  border-radius: 30px;
  transition: 500ms;
}

</style>