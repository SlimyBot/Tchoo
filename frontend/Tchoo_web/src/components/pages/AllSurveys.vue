<script setup>
import Gear from "@/components/Gear.vue";
import ClearButton from "../ClearButton.vue";
import { ref, computed, onMounted } from "vue";
import { getSurveys, getQuestionsBank, createSurvey, createQuestion, getAllSessionTemplates, createSessionTemplate, createAnswer, linkQuestion, updateQuestion } from "../../lib/requests.js";
import SurveyDetails from './survey/SurveyDetails.vue';
import { useRouter } from "vue-router";
import Header from '@/components/Header.vue';
import { parse } from "gift-pegjs";


const router = useRouter();
const selectedSurvey = ref(null);
const currentDisplay = ref('surveys');
const surveys = ref([]);
const questionBank = ref([]);
const selectedOption = ref('Quizz');
const fileInputRef = ref(null);

const searchQuery = ref('');
const sessionTemplates = ref([])
const selectedTemplate = ref(null)


const fetchSurveys = async () => {
  try {
    const [data, status] = await getSurveys();
    if (status === 200) {
      return data;
    } else {
      console.error("Erreur de récupération des questionnaires : Statut ", status);
      return null;
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des questionnaires", error);
    return null;
  }
};

const fetchSessionTemplates = async () => {
  try {
    const [data, status] = await getAllSessionTemplates();
    if (status === 200) {
      return data;
    } else {
      console.error("Erreur lors de la récupération des modèles de session : Statut ", status);
      return null;
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des modèles de session", error);
    return null;
  }
};

const loadAllSurveys = async () => {
  const surveysData = await fetchSurveys();
  if (surveysData) {
    surveys.value = surveysData;
  }

  const templateData = await fetchSessionTemplates();
  if (templateData) {
    sessionTemplates.value = templateData;
  }
};


onMounted(loadAllSurveys)

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

function selectSurvey(survey) {
  selectedSurvey.value = survey;
}

function selectTemplate(template) {
  selectedTemplate.value = template
}

function onTemplateDelete() {
  selectedTemplate.value = null
  loadAllSurveys()
}

function handleSelectChange() {
  if (selectedOption.value === 'Quizz') {
    currentDisplay.value = 'surveys';
  } else if (selectedOption.value === 'Question') {
    currentDisplay.value = 'questionBank';
    loadQuestionBank();
  } else {
    currentDisplay.value = "templates";
  }
}

async function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      const content = event.target.result;
      resolve(content);
    };

    reader.onerror = (error) => {
      reject(error);
    };

    reader.readAsText(file);
  });
}

function handleGiftFileChange(event) {
  fileInputRef.value = event.target;
  importQuestions();
}

function handleAmcFileChange(event) {
  fileInputRef.value = event.target
  importSurvey();
}

function onSurveyDelete() {
  selectedSurvey.value = null;
  loadAllSurveys();
}

function parseAmc(amcString) {
  const surveys = [];
  let currentSurvey = null;

  const lines = amcString.split("\n");

  for (let index = 0; index < lines.length; index++) {
    const trimmedLine = lines[index].trim();

    if (trimmedLine === "" || trimmedLine.startsWith("#")) {
      continue;
    }

    if (trimmedLine.startsWith("Title:")) {
      if (currentSurvey) {
        surveys.push({ ...currentSurvey });
      }

      currentSurvey = {
        name: trimmedLine.split(":")[1].trim(),
        questions: [],
        subject: null,
      };
    }

    if (trimmedLine.startsWith("Presentation:")) {
      const presentationText = trimmedLine.split(":")[1].trim();

      currentSurvey.subject = {
        type: "presentation",
        text: presentationText + " ",
      };

      index++;
      let subjectText = "";

      while (index < lines.length && lines[index].trim() !== "") {
        subjectText += lines[index] + " ";
        index++;
      }


      currentSurvey.subject.text += subjectText.trim();
      index--;
    }

    if (trimmedLine.startsWith("*") || trimmedLine.startsWith("**")) {
      const questionParts = trimmedLine.split(/(\*\*|\*)/).filter(Boolean);
      const isMultipleChoice = questionParts[0].includes("**");

      const questionText = questionParts.slice(1).join("").trim() + " ";
      const isCorrect = "+";

      if (questionText !== "") {
        const question = {
          text: questionText,
          type: isMultipleChoice ? "multiple_answers" : "single_answer",
          answers: [],
        };

        index++;

        while (index < lines.length && !lines[index].startsWith("*")) {
          const answerLine = lines[index].trim();

          if (answerLine !== "") {
            const symbol = answerLine.charAt(0);
            const answerText = answerLine.slice(1).trim();

            question.answers.push({
              text: answerText,
              isCorrect: symbol === isCorrect,
            });
          }

          index++;
        }


        currentSurvey.questions.push({ ...question });
        index--;
      }
    }
  }

  if (currentSurvey) {
    surveys.push({ ...currentSurvey });
  }

  return surveys;
}


async function importQuestions() {
  const fileInput = fileInputRef.value;
  const file = fileInput.files[0];
  let questionType = 0;

  if (!file) {
    return;
  }

  const content = await readFile(file);
  const questions = await parse(content);

  for (const question of questions) {
    const createdQuestion = await createQuestion("open", question.stem.text, "no media");

    if (!(question.choices)) {
      continue;
    }
    for (const answer of question.choices) {
      await createAnswer(createdQuestion[0].id, answer.text.text, answer.isCorrect);
      if (answer.isCorrect) {
        questionType++;
        await updateQuestion(createdQuestion[0].id, question.stem.text, "no media", "single_answer");
      }
      if (questionType > 1) {
        await updateQuestion(createdQuestion[0].id, question.stem.text, "no media", "multiple_answers");
      }
    }
    questionType = 0;

  }

  fileInput.value = null;
  loadAllSurveys();
}

async function importSurvey() {
  const fileInput = fileInputRef.value;
  const file = fileInput.files[0];

  if (!file) {
    return;
  }

  const content = await readFile(file);
  const surveys = parseAmc(content);

  for (const survey of surveys) {
    const createdSurvey = await createSurvey(survey.name, survey.subject.text);

    for (const question of survey.questions) {
      const createdQuestion = await createQuestion(question.type, question.text, "no media");
      await linkQuestion(createdQuestion[0].id, createdSurvey[0].id);

      for (const answer of question.answers) {
        await createAnswer(createdQuestion[0].id, answer.text, answer.isCorrect);
      }
    }
  }

  fileInput.value = null;
  loadAllSurveys();
}


async function handleCreation() {
  if (selectedOption.value === 'Quizz') {
    const createSurv = await createSurvey("", "");
    router.push('/survey/' + createSurv[0].id);
  } else if (selectedOption.value === 'Question') {
    const createQuest = await createQuestion("multiple_answers", "", "no media");
    router.push('/createQuestion/' + createQuest[0].id);
  }
}

const filteredSurveys = computed(() => {
  return surveys.value.filter(survey =>
    survey.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const filteredQuestions = computed(() => {
  return questionBank.value.filter(question =>
    question.text.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});


</script>

<template>
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <div>
    <Header />
    <div class="top-part">
      <div class="left-part">
        <hr>
        <div class="bottom-left">
          <div class="search-container">
            <label>
              <p style="display: none">Searchbar</p>
              <input v-model="searchQuery"
                     type="text"
                     class="search"
              >
              <img src="../../assets/magnifying-glass.svg"
                   alt=""
              >
            </label>
          </div>
          <select v-model="selectedOption"
                  class="selectFilter"
                  @change="handleSelectChange"
          >
            <option value="Quizz">
              {{ $t("survey.surveys") }}
            </option>
            <option value="Question">
              {{ $t("survey.questions") }}
            </option>

            <option value="Sessions">
              {{ $t("survey.sessionsShow") }}
              <!-- Voir mes modèles de sessions -->
            </option>
          </select>
        </div>
      </div>

      <div class="ImportButtons">
        <div class="importDiv">
          <label class="custom-file-upload">
            <input ref="importFile"
                   type="file"
                   class="importFile"
                   @change="handleGiftFileChange"
            >
            {{ $t("survey.import") }}
            <!-- Importer des questions -->
          </label>
        </div>
        <div class="importDiv">
          <label class="custom-file-upload">
            <input ref="importFile"
                   type="file"
                   class="importFile"
                   @change="handleAmcFileChange"
            >
            {{ $t("survey.importSurvey") }}
            <!-- Importer un questionnaire -->
          </label>
        </div>
      </div>

      <div class="handle-my-stuff">
        <ClearButton to="AllSessions">
          {{ $t("survey.session") }}
        </ClearButton>
        <ClearButton to="/groups">
          {{ $t("survey.groups") }}
        </ClearButton>
      </div>
    </div>

    <!-- Ecran pour afficher la liste des questionaires -->
    <div v-if="currentDisplay === 'surveys'"
         class="wrappable-parent"
    >
      <div class="new survey">
        <div @click="handleCreation()">
          <svg xmlns="http://www.w3.org/2000/svg"
               fill="none"
               viewBox="0 0 24 24"
               stroke-width="1.5"
               stroke="currentColor"
          >
            <path stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
        </div>
      </div>

      <!-- Construit automatiquement la liste des questionnaires-->
      <div v-for="survey in filteredSurveys"
           :key="survey.id"
           class="survey"
           @click="selectSurvey(survey)"
      >
        <h3 class="title">
          {{ survey.title && survey.title.trim() !== '' ? survey.title : 'no title' }}
        </h3>
        <p>{{ $t("survey.subject") }} : {{ survey.subject }}</p>
      </div>

      <SurveyDetails :survey="selectedSurvey"
                     @survey-delete="onSurveyDelete()"
      />
    </div>

    <!-- Ecran pour afficher la liste des questions dans la banque -->
    <div v-if="currentDisplay === 'questionBank'"
         class="wrappable-parent"
    >
      <div class="new survey">
        <div @click="handleCreation()">
          <svg xmlns="http://www.w3.org/2000/svg"
               fill="none"
               viewBox="0 0 24 24"
               stroke-width="1.5"
               stroke="currentColor"
          >
            <path stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
        </div>
      </div>

      <div v-for="question in filteredQuestions"
           :key="question.id"
           class="survey"
           @click="router.push('/createQuestion/' + question.id)"
      >
        <h3 class="title">
          {{ question.text && question.text.trim() !== '' ? question.text : 'untitled' }}
        </h3>
        <p>{{ $t("survey.media") }} : {{ question.media }}</p>
      </div>
    </div>

    <!-- Liste des modèles de sessions -->
    <div v-if="currentDisplay === 'templates'"
         class="wrappable-parent"
    >
      <div v-for="template in sessionTemplates"
           :key="template.id"
           class="survey"
           @click="selectTemplate(template)"
      >
        <h3 class="title">
          {{ template.name }}
        </h3>
        <div class="template-options">
          <div v-if="template && template.type === 'piloted'"
               class="template-pill"
          >
            {{ $t("survey.piloted") }}
          </div>  
          <div v-else-if="template && template.type === 'auto_timer'"
               class="template-pill"
          >
            {{ $t("survey.auto_timer") }}
          </div>
          <div v-else="template && template.type === 'auto_free'"
               class="template-pill"
          >
            {{ $t("survey.auto_free") }}
          </div>

          <div class="template-pill">
            {{ template.authorised_group_id === null ? $t('survey.Publique') : $t('survey.Privé') }}
          </div>
          <div class="template-pill">
            {{ template.show_answers ? $t('survey.hide') : $t('survey.show') }}
          </div>
        </div>
      </div>

      <SurveyDetails :survey="selectedTemplate"
                     @survey-delete="onTemplateDelete()"
      />
    </div>

    <Gear />
  </div>
</template>

<style scoped>
.template-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1em;
}

.template-pill {
  background-color: white;
  padding: 0.5em;
  border-radius: 9999px;
}

.survey:hover div {
  color: white;
}

.template-pill {
  border: var(--CTA-color) 1px solid;
  color: var(--CTA-color);
}

.survey:hover .template-pill {
  border: var(--white) 1px solid;
  background-color: var(--CTA-color);
}

* {
  font-family: "Sofia Sans", sans-serif;
}

.top-part {
  display: flex;
  gap: 2em;
  padding: 2px 1.5em;
}

hr {
  border: none;
  height: 1px;
  width: 100%;
  background-color: lightgray;
}

.left-part {
  flex-grow: 1;
  display: flex;
  gap: 1em;
  flex-direction: column;
  justify-content: space-between;
}

.bottom-left {
  display: flex;
  flex-direction: row;
  gap: 2em;
}

.search-container {
  flex-grow: 1;
  position: relative;
  color: var(--text-color);
}

.search-container img {
  position: absolute;
  top: 0;
  right: 0;
  width: 20px;
  padding: 10px 0px 0px 10px;
  height: auto;
  filter: var(--filter);
}

.search {
  width: 100%;
  height: 1.90em;
  border-radius: 20px;
  border: 1px solid var(--main-color);
  padding: 6px 2px 2px 10px;
  font-family: "Sofia Sans", sans-serif;
  font-size: medium;
  background-color: var(--background);
}

.handle-my-stuff {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
  justify-content: space-between;
}

.importDiv {
  display: flex;
  flex-direction: column;
  justify-content: end;
}

.ImportButtons {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1em;
}

.custom-file-upload {
  display: inline-block;
  padding: 10px 20px;
  cursor: pointer;
  background-color: var(--CTA-color);
  border: 1px solid var(--CTA-color);
  border-radius: 30px;
  color: white;
}

.custom-file-upload span {
  margin-right: 10px;
}

.custom-file-upload:hover {
  background-color: var(--CTA-color);
  color: white;
  transition: linear 0.3s;
}

.importFile {
  display: none;
}

div>.survey {
  border: solid 1px var(--main-color);
}

@media (max-width: 500px) {
  .top-part {
    flex-direction: column;
  }

  .bottom-left {
    flex-direction: row;
    width: 100%;
  }

  .search-container {
    width: 10vw;
  }

  .ImportButtons {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .selectFilter {
    width: 100%;
  }

}

@media screen and (max-width: 400px) {
  .bottom-left {
    flex-direction: column;
  }

  .ImportButtons {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .selectFilter {
    width: 100%;
  }
}

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
  color: var(--text-color);
  min-width: 30vw;
  padding: 10px;
  background-color: var(--white);

  font-family: "Sofia Sans", sans-serif;

  max-width: 200px;
  width: 100%;
  height: 200px;

  transition: 0.2s;
}

.survey:not(.new) {
  overflow-y: auto;
}

.survey:hover {
  background-color: var(--CTA-color);
  color: white !important;
  transition: 0.1s;
}

.new.survey {
  background-color: var(--white);
}

/* le router-link */
.new div {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.new svg {
  color: var(--text-color);
  width: 40px;
  height: auto;
  transition: 0.3s;
}

.new:hover svg {
  transform: scale(1.3);
}

p {
  word-break: break-word;
}

.title {
  word-break: break-word;
}

.title::first-letter {
  text-transform: uppercase;
}

.selectFilter {
  width: 20vw;
  height: 40px;
  border: 1px solid var(--main-color);
  font-family: "Sofia Sans", sans-serif;
  color: var(--text-color);
  background-color: var(--white);
  border-radius: 25px;
  text-align-last: center;
  transition: 700ms;
}

.selectFilter option {
  height: 50px;
}

button {
  border-radius: 30px;
  background-color: var(--white);
  border: 2px solid var(--CTA-color);
  cursor: pointer;
  margin-left: 50px;
  margin-right: 10px;
  padding: 15px;
  margin-bottom: 10px;
}

button:hover {
  background-color: var(--CTA-color);
  color: var(--white);
  transition: linear 0.3s;
}
</style>
