<script setup>
import { ref, onMounted, inject } from 'vue';
import { getSurveys } from '../../../lib/requests.js';

const allSurveys = ref([]);
const template = inject("template")
const searchQuery = ref("");

const emits = defineEmits(["surveyChoosed"])

onMounted(async () => {
  await loadSurveys();
});

async function loadSurveys() {
  try {
    const [surveysData, surveysStatus] = await getSurveys();
    if (surveysStatus === 200) {
      allSurveys.value = surveysData;
    } else {
      console.error("Erreur de récupération des questionnaires : Statut ", surveysStatus);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des questionnaires", error);
  }
}

function selectSurvey(survey) {
  template.value.survey_id = survey.id;
  emits("surveyChoosed")
}

function filterSurveys() {
  if (!searchQuery.value) {
    return allSurveys.value;
  }

  return allSurveys.value.filter(survey =>
    survey.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
}
</script>

<template>
  <input v-model="searchQuery"
         class="search"
         type="text"
         :placeholder="$t('survey.researchSurvey')"
  >
  <!-- <input v-model="searchQuery"
         class="search"
         type="text"
         placeholder="Rechercher un questionaire..."
  > -->

  <div class="wrappable-parent">
    <div
      v-for="survey in filterSurveys()"
      :key="survey.id"
      class="survey"
      @click="selectSurvey(survey)"
    >
      <h3 class="title">
        {{ survey.title }}
      </h3>
      <p>{{ $t ("survey.subject") }}  : {{ survey.subject }}</p>
    </div>
  </div>
  <!-- <button v-if="selectedSurveyId" class="button" @click="validerSelection">
    Ajouter
  </button> -->
</template>

<style scoped>
.wrappable-parent {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin: 1em 0;
  gap: 2em;
}

.survey {
  border-radius: 10px;
  border: var(--CTA-color) 1px solid;

  cursor: pointer;
  min-width: 30vw;
  padding: 10px;
  background-color: var(--white);

  font-family: "Sofia Sans", sans-serif;

  max-width: 200px;
  width: 100%;
  height: 200px;
}

.search {
  width: 60%;
  height: 1.75em;
  border-radius: 20px;
  border: 1px solid var(--CTA-color);
  padding: 2px 10px;
  padding-right: 2px;
  margin-top: 0.75em;
  margin-left: auto;
  margin-right: auto;
  display: flex;
}

.survey:hover {
  background-color: var(--CTA-color);
  color: var(--white);
  transition: 0.5s;
}

.survey.selected {
  background-color: var(--CTA-color);
  color: var(--white);
  transition: 0.5s;
}

button {
  margin-left: auto;
  margin-right: auto;
  margin-top: 1em;
  display: flex;
  border-radius: 20px;
  border: 1px solid var(--CTA-color);
  background-color: white;
  padding: 0.5em 2em;
  text-decoration: none;
  color: var(--text-color);
  font-family: "Sofia Sans", sans-serif;
}

button:hover {
  cursor: pointer;
  background-color: var(--CTA-color);
  color: var(--white);
  transition: 700ms;
}
</style>