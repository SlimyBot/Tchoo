<script setup>
import { ref, onMounted, inject } from 'vue';
import { getQuestionsBank } from '../../../lib/requests.js';

const questionBank = ref([]);
const selectedQuestionIds = inject('selectedQuestionIds');
const searchQuery = ref('');
const validerSelection = inject('validerSelection');

onMounted(async () => {
  await loadQuestionBank();
});

async function loadQuestionBank() {
  try {
    const [questionBankData, questionBankStatus] = await getQuestionsBank();
    if (questionBankStatus === 200) {
      questionBank.value = questionBankData;
      //answers.value = questionBankData.answers || [];
    } else {
      console.error("Erreur de récupération des questions : Statut ", questionBankStatus);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des questions", error);
  }
}

function selectQuestion(questionId) {
  const index = selectedQuestionIds.value.indexOf(questionId);
  if (index > -1) {
    selectedQuestionIds.value.splice(index, 1); // Retirer l'ID si déjà présent
  } else {
    selectedQuestionIds.value.push(questionId); // Ajouter l'ID s'il n'est pas déjà présent
  }
}

function filterQuestions() {
  if (!searchQuery.value) {
    return questionBank.value;
  }
  return questionBank.value.filter(question =>
    question.text.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
}
</script>

<template>
  <input v-model="searchQuery"
         class="search"
         type="text"
         :placeholder="$t('survey.research')"
  >
  <!-- <input v-model="searchQuery"
         class="search"
         type="text"
         placeholder="Rechercher une question..."
  > -->
  <div
    
    class="wrappable-parent"
  >
    <div
      v-for="question in filterQuestions()"
      :key="question.id"
      class="survey"
      :class="{ selected: selectedQuestionIds.includes(question.id) }"
      @click="selectQuestion(question.id)"        
    > 
      <h3 class="title">
        {{ question.text }}
      </h3>
      <p>{{ $t ("survey.media") }}  : {{ question.media }}</p>
    </div>
  </div>
  <button v-if="selectedQuestionIds.length > 0"
          class="button"
          @click="validerSelection"
  >
    {{ $t("survey.add") }}
    <!-- Ajouter -->
  </button>
</template>

<style scoped>

.wrappable-parent {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin: 1em 0;
  gap: 2em;
  max-height: 450px;
  overflow-y: auto;
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