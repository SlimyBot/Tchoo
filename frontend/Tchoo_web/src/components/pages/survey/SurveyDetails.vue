<script setup>
import { ref, watch } from 'vue';
import { useRouter } from "vue-router";
import { getSurvey, deleteSurvey, createSessionTemplate, startSurveySession, deleteSessionTemplate } from '@/lib/requests.js';

const router = useRouter()

const emit = defineEmits(["surveyDelete"])

const props = defineProps({
  survey: {
    type: Object,
    default: () => ({})
  }
});

const isReduced = ref(false);
const questions = ref([]);
const questionCount = ref(0);
const isTemplate = ref(false)

function loadSurveyDetails() {
  if (props.survey && props.survey.id && !props.survey.survey_id) {
    getSurvey(props.survey.id).then(questionsList => {
      questions.value = questionsList;
      questionCount.value = questionsList[0].length;
      isTemplate.value = false
    }).catch(error => {
      console.error("Erreur lors de la récupération des questions", error);
    });
  } else {
    // Modèle de session
    isTemplate.value = true
  }
}

watch(() => props.survey, (newVal) => {
  //decommenter pour voir les changements de props
  //console.log("Survey prop updated:", newVal);
  loadSurveyDetails(); // Appelle la fonction lorsque le prop survey est mis à jour
}, { deep: true });

function toggleMenu() {
  isReduced.value = !isReduced.value;
}

function handleDeleteSurvey() {
  deleteSurvey(props.survey.id).then(() => {
    console.log("Survey deleted");

    emit("surveyDelete")
  }).catch(error => {
    console.error("Erreur lors de la suppression du questionnaire", error);
  });
}

async function handleDeleteTemplate() {
  await deleteSessionTemplate(props.survey.id)
  emit("surveyDelete")
}

function handleEditSurvey() {
  router.push({
    name: 'EditSurvey',
    params: {
      id: props.survey.id
    }
  });
}

async function createSurveySessionTemplate(surveyId) {
  const [createdTemplate, status] = await createSessionTemplate(surveyId, "Nouveau modèle")

  if (status !== 200) {
    alert("Erreur lors de la création d'un modèle de session");
    console.error(createdTemplate);
    return;
  }

  router.push("/template/" + createdTemplate.id)
}

async function startQuickSession(surveyId) {
  let [json, status] = await createSessionTemplate(surveyId, "Session à l'improviste");

  if (status !== 200) {
    alert("Erreur lors de la création d'une session a l'improviste (voir console)");
    console.error(json);
    return;
  }

  const templateId = json["id"];
  [json, status] = await startSurveySession(templateId);
  const joinCode = json["join_code"];

  console.log("Session lancée a l'improviste : " + joinCode);
  router.push("/session/" + joinCode);
}

async function startSessionTemplate() {
  const [json, _] = await startSurveySession(props.survey.survey_id);
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


  <div
    v-if="survey && Object.keys(survey).length > 0"
    class="burger-menu"
    :class="{ 'reduced': isReduced }"
  >
    <div v-if="!isReduced">
      <div class="align">
        <p class="title">
          {{ survey.title }}
        </p>
        <button>
          <span class="material-symbols-outlined">
            share
          </span>
        </button>
      </div>

      <div
        v-if="!isTemplate"
        class="survey-stuff"
      >
        <p><b>{{ $t("surDetails.subject") }}</b>: {{ survey.subject }}</p>
        <p><b>{{ $t("surDetails.nbrQuestion") }}</b>: {{ questionCount }}</p>
      </div>

      <!-- Mode questionaire -->
      <div
        v-if="!isTemplate"
        class="center"
      >
        <button
          class="actionBtn deleteBtn"
          @click="handleDeleteSurvey()"
        >
          <span class="material-symbols-outlined">
            delete
          </span>
          {{ $t ("surDetails.delete") }} 
        </button>

        <button
          class="actionBtn"
          @click="router.push('/survey/'+survey.id)"
        >
          <span class="material-symbols-outlined">
            edit
          </span>
          {{ $t ("surDetails.edit") }}
          <!-- Modifier le questionaire -->
        </button>

        <button
          class="actionBtn"
          @click="createSurveySessionTemplate(survey.id)"
        >
          <span class="material-symbols-outlined">
            add_circle
          </span>
          {{ $t ("surDetails.create") }}
          <!-- Créer une session -->
        </button>

        <button
          class="actionBtn"
          @click="startQuickSession(survey.id)"
        >
          <span class="material-symbols-outlined">
            start
          </span>
          {{ $t ("surDetails.quick")  }}
          <!-- Session à l'improviste -->
        </button>
      </div>

      <!-- Mode modèle de session -->
      <div
        v-else
        class="center"
      >
        <button
          class="actionBtn deleteBtn"
          @click="handleDeleteTemplate()"
        >
          <span class="material-symbols-outlined">
            delete
          </span>
          {{ $t ("surDetails.delete") }} 
        </button>

        <button
          class="actionBtn"
          @click="router.push('/template/'+survey.id)"
        >
          <span class="material-symbols-outlined">
            edit
          </span>
          {{ $t ("surDetails.editSession")  }}
          <!-- Modifier le modèle de session -->
        </button>

        <button
          class="actionBtn"
          @click="startSessionTemplate()"
        >
          <span class="material-symbols-outlined">
            start
          </span>
          {{ $t ("surDetails.startSession")  }}
          <!-- Lancer une session -->
        </button>
      </div>
    </div>

    <button @click="toggleMenu">
      <span class="material-symbols-outlined">
        expand_content
      </span>
    </button>
  </div>
</template>

<style scoped>
.burger-menu {
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  background-color: var(--white);
  color: var(--black);
  padding: 10px 20px;
  border-radius: 10px 10px 0 0;
  border: var(--CTA-color) 1px solid;
  box-shadow: var(--CTA-color) 0 0 1px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.burger-menu.reduced {
  padding: 10px;
  width: 50px;
  height: 50px;
  border-radius: 50%; /* Rend le menu circulaire */
  display: flex;
  align-items: center;
  justify-content: center;
}

.burger-menu button {
  background: none;
  border: none;
  color: var(--black);
  cursor: pointer;
}

.title {
  font-weight: bold;
  font-size: 1.2em;
  text-align: center;
  flex-grow: 1;
}

.title::first-letter {
  text-transform: uppercase;
}

.center {
  display: flex;
  justify-content: center;
}

.align {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.deleteBtn {
  background-color: var(--CTA-2-color);
  border: none;
}

.deleteBtn img {
  width: 20px;
  height: auto;
}

.actionBtn {
  background-color: var(--CTA-color);
  color: var(--white);
  border: none;
  padding: 5px 10px;
  margin: 0 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

* {
  font-family: 'Sofia Sans', sans-serif;
  color: var(--text-color);
}
.material-symbols-outlined {
  font-variation-settings:
      'FILL' 0,
      'wght' 200,
      'GRAD' 0,
      'opsz' 40
}
</style>
