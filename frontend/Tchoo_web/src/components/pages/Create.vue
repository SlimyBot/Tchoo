<script setup>
import { ref, computed, provide, watch, nextTick, onMounted } from 'vue';
import Gear from "@/components/Gear.vue";
import { createQuestion, createAnswer, deleteAnswer, linkQuestion, unlinkQuestion, getSurvey, getQuestion, updateQuestion, updateAnswer, updateSurvey, getSurveyInfo } from '../../lib/requests.js';
import { useRouter, useRoute } from "vue-router";
import ImportQuestion from './survey/ImportQuestion.vue';
import Header from '@/components/Header.vue';

const router = useRouter();
const route = useRoute();
const surveyId = route.params.id;
const pages = ref([{ question: 'Question texte', time: 60 }]);
const currentPageIndex = ref(0);
const newAnswers = ref(['']);
const correctAnswers = ref([]);
const surveyDescription = ref();
const surveyTitle = ref();
const questionType = ref('multiple_answers');
const listQuestionObject = {
  questions: []
};
const listQuestionId = [];
const listAnswerId = [];
const currentDisplay = ref('cancelQuestionBank');
const selectedQuestionIds = ref([]);
const question = ref();
const selectedOption = ref('save');
const selectedQuestionCount = ref(1);
const questionCountOptions = [1, 2, 3, 4, 5, 6, 7, 8];
provide('selectedQuestionIds', selectedQuestionIds);
provide('validerSelection', validerSelection);

onMounted(async () => {
  await buildListQuestionId(surveyId);
  const currPage = currentPageIndex.value;
  //pages.value[currPage].question = listQuestionObject.questions[currPage-1].questionText;
  const survey = await getSurveyInfo(surveyId);
  surveyTitle.value = survey[0].title;
  surveyDescription.value = survey[0].subject;
  if (listQuestionObject.questions.length > 0){
    question.value = listQuestionObject.questions[currPage].questionText;
    questionType.value= listQuestionObject.questions[currPage].questionType;
    newAnswers.value = listQuestionObject.questions[currPage].answers.map(a => a.answer);
    correctAnswers.value = listQuestionObject.questions[currPage].correctAnswers;
    updateCheckboxes();
    selectedQuestionIds.value = [];
  }
  
});

async function buildListQuestionId(surveyId) {
  const questions = await getSurvey(surveyId);
  if (questions[0].length === 0) return;
  currentPageIndex.value = 0;
  for (let i = 0; i < questions[0].length; i++) {
    const question = questions[0][i];
    pages.value.splice(i, 1, { question: 'Question texte', time: 60 });
    listQuestionId.push(question.id);
  }
  await buildListQuestionObject(listQuestionId);
}

async function buildListQuestionObject(listQuestionId) {
  for (let i = 0; i < listQuestionId.length; i++) {
    const question = await getQuestion(listQuestionId[i]);
    const answerstemp = question[0][1];
    const questionObject = {
      questionText: question[0][0].text,
      questionType: question[0][0].type,
      answers: [],
      correctAnswers: [],
      questionId: question[0][0].id, 
    };
    for (let j = 0; j < answerstemp.length; j++) {
      questionObject.answers.push({
        answer : answerstemp[j].text,
        answerId : answerstemp[j].id});
      if (answerstemp[j].is_correct) {
        questionObject.correctAnswers.push(j);
      }
    }
    listQuestionObject.questions.push(questionObject);
  }
}

async function saveSurvey() {
  addQuestionToList();
  await updateSurvey(surveyId, surveyTitle.value, surveyDescription.value);

  for (let i = 0; i < listQuestionObject.questions.length; i++) {
    const questionObject = listQuestionObject.questions[i];

    let questionId;
    if (questionObject.questionId === null) {
      const response = await createQuestion(questionObject.questionType, questionObject.questionText, "no media");
      questionId = response[0].id;
      await linkQuestion(questionId, surveyId);
    } else {
      questionId = questionObject.questionId;
      await updateQuestion(questionId, questionObject.questionText, "no media", questionType.value);
    }

    for (let j = 0; j < questionObject.answers.length; j++) {
      const answer = questionObject.answers[j];
      const isCorrectAnswer = questionObject.correctAnswers.includes(j);
            
      if (answer.answerId === null) {
        await createAnswer(questionId, answer.answer, isCorrectAnswer);
      } else {
        await updateAnswer(answer.answerId, answer.answer, isCorrectAnswer);
      }
    }
  }
  router.push('/surveys');
}

async function updateQuestions() {
  const currentLength = newAnswers.value.length;
  const newLength = selectedQuestionCount.value;

  if (newLength > currentLength) {
    // Ajouter des éléments vides jusqu'à ce que la longueur corresponde
    for (let i = currentLength; i < newLength; i++) {
      newAnswers.value.push('');
    }
  } else if (newLength < currentLength) {
    // Supprime les answers en trop avec leurs id à l'aide de deleteAnswer
    for (let i = newLength; i < currentLength; i++) {
      const answerObject = listQuestionObject.questions[currentPageIndex.value].answers[i];
      if (answerObject && answerObject.answerId !== undefined) {
        await deleteAnswer(answerObject.answerId);
      }
    }
    newAnswers.value = newAnswers.value.slice(0, newLength);
    listQuestionObject.questions[currentPageIndex.value].answers = listQuestionObject.questions[currentPageIndex.value].answers.slice(0, newLength);
  }
};


const remvPage = () => {
  goToPreviousPage();
  removeLastQuestionFromList();
  if (pages.value.length > 1) {
    pages.value.pop();
    if (currentPageIndex.value >= pages.value.length) {
      currentPageIndex.value = pages.value.length - 1;
    }
  }
};

const addNewPage = () => {
  addQuestionToList();
  //reset des var de question et answers
  question.value = '';
  questionType.value = 'multiple_answers';
  newAnswers.value = [''];
  pages.value.push({ question: 'Question texte', time: 60 });
  currentPageIndex.value = pages.value.length - 1;
  selectedQuestionCount.value = 1;
  const checkboxes = document.querySelectorAll('.check');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;   
  });
};

const goToPreviousPage = () => {
  addQuestionToList();
  displayLeftQuestion();

  if (currentPageIndex.value > 0) {
    currentPageIndex.value--;
  }
};

const goToNextPage = () => {
  addQuestionToList();
  displayRightQuestion();
  if (currentPageIndex.value < pages.value.length - 1) {
    currentPageIndex.value++;
  }
};

function displayRightQuestion() {
  const currPage = currentPageIndex.value;
  if (currPage < listQuestionObject.questions.length - 1) {
    question.value = listQuestionObject.questions[currPage + 1].questionText;
    questionType.value = listQuestionObject.questions[currPage + 1].questionType;
    newAnswers.value = listQuestionObject.questions[currPage + 1].answers.map(a => a.answer);
    correctAnswers.value = listQuestionObject.questions[currPage + 1].correctAnswers;
    updateCheckboxes();
  }

};

function displayLeftQuestion() {
  const currPage = currentPageIndex.value;
  if (currPage > 0) {
    question.value = listQuestionObject.questions[currPage - 1].questionText;
    questionType.value = listQuestionObject.questions[currPage - 1].questionType;
    newAnswers.value = listQuestionObject.questions[currPage - 1].answers.map(a => a.answer);
    correctAnswers.value = listQuestionObject.questions[currPage - 1].correctAnswers;
    updateCheckboxes();
  }
}

function updateCheckboxes() {
  selectedQuestionCount.value = newAnswers.value.length;
  nextTick(() => {
    const checkboxes = document.querySelectorAll('.check');
    checkboxes.forEach((checkbox, index) => {
      checkbox.checked = correctAnswers.value.includes(index);
    });
  });
}

function addQuestionToList() {
  const questionText = question.value;
  const answerElements = document.querySelectorAll('.answerSelect');
  const checkboxes = document.querySelectorAll('.check');
  let questId = listQuestionObject.questions[currentPageIndex.value] && listQuestionObject.questions[currentPageIndex.value].questionId
    ? listQuestionObject.questions[currentPageIndex.value].questionId
    : null;   

  // Remplacer ou ajouter la question dans la liste à l'index courant
  if (currentPageIndex.value < listQuestionObject.questions.length) {
    const questionObject = {
      questionText,
      questionType: questionType.value,
      answers: [],
      correctAnswers: [],
      questionId: questId
    };

    if (answerElements.length !== listQuestionObject.questions[currentPageIndex.value].answers.length) {
      for (let i = 0; i < listQuestionObject.questions[currentPageIndex.value].answers.length; i++) {
        questionObject.answers.push({answer: answerElements[i].value, answerId: listQuestionObject.questions[currentPageIndex.value].answers[i].answerId});
        if (checkboxes[i].checked) {
          questionObject.correctAnswers.push(i);
        }
      }
      for (let i = listQuestionObject.questions[currentPageIndex.value].answers.length; i < answerElements.length; i++) {
        questionObject.answers.push({answer: answerElements[i].value, answerId: null});
        if (checkboxes[i].checked) {
          questionObject.correctAnswers.push(i);
        }
      }
    }
    else{
      answerElements.forEach((answerElement, index) => {
        questionObject.answers.push({
          answer: answerElement.value,
          answerId: listQuestionObject.questions[currentPageIndex.value].answers[index].answerId
        });
        if (checkboxes[index].checked) {
          questionObject.correctAnswers.push(index);
        }
      });
    }
    listQuestionObject.questions.splice(currentPageIndex.value, 1, questionObject);
        
  } else {
    const questionObject = {
      questionText,
      questionType: questionType.value,
      answers: [],
      correctAnswers: [],
      questionId: null
    };

    answerElements.forEach((answerElement, index) => {
      questionObject.answers.push({answer: answerElement.value, answerId: null});
      if (checkboxes[index].checked) {
        questionObject.correctAnswers.push(index);
      }
    });
    listQuestionObject.questions.push(questionObject);
  }
}
async function removeLastQuestionFromList() {
  //supprime le dernier de listQuestionObject
  try {
    await unlinkQuestion(listQuestionId[currentPageIndex.value], surveyId);
  } catch (error) {
    console.error('Erreur lors de la dissociation de la question :', error);
  }
  listQuestionObject.questions.pop();
};

function updateListAnswer(event, index) {
  newAnswers.value[index] = event.target.value;
}

async function deleteCurrentQuestion() {
  if (listQuestionId[currentPageIndex.value] !== undefined) {
    try {
      await unlinkQuestion(listQuestionId[currentPageIndex.value], surveyId);
      listQuestionId.splice(currentPageIndex.value, 1)
    } catch (error) {
      console.error('Erreur lors de la dissociation de la question :', error);
    }
  }

  listQuestionObject.questions.splice(currentPageIndex.value, 1);

  if (listQuestionObject.questions.length === 0) {
    resetQuestionForm();
    currentPageIndex.value = 0;
    return;
  }

  if (currentPageIndex.value >= listQuestionObject.questions.length) {
    currentPageIndex.value = listQuestionObject.questions.length - 1;
  }

  updateQuestionForm(currentPageIndex.value);
}

function resetQuestionForm() {
  question.value = '';
  newAnswers.value = [''];
  correctAnswers.value = [''];
  selectedQuestionCount.value = 1;
  uncheckAllCheckboxes();
}

function updateQuestionForm(index) {
  const currentQuestion = listQuestionObject.questions[index];
  question.value = currentQuestion.questionText;
  questionType.value = currentQuestion.questionType;
  newAnswers.value = currentQuestion.answers.map(a => a.answer);
  correctAnswers.value = currentQuestion.correctAnswers;
  updateCheckboxes();
}

function uncheckAllCheckboxes() {
  const checkboxes = document.querySelectorAll('.check');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
}


function autoExpand(event) {
  event.target.style.height = 'inherit'; // Réinitialise la hauteur
  event.target.style.height = `${event.target.scrollHeight}px`;
}

function handleImportQuestion() {
  if (currentDisplay.value === 'QuestionBank'){
    currentDisplay.value = 'CancelQuestionBank';
  }else{
    currentDisplay.value = 'QuestionBank';
  }
}

async function validerSelection() {
  for (const questionId of selectedQuestionIds.value) {
    // Lier chaque question sélectionnée au sondage
    try {
      await linkQuestion(questionId, surveyId);
    } catch (error) {
      console.error('Erreur lors de la liaison de la question :', error);
      return;
    }
    pages.value.push({ question: 'Question texte', time: 60 });

    const selectedQuestion = await getQuestion(questionId);
    const answerstemp = selectedQuestion[0][1];
    // Construire l'objet de la question
    const questionObject = {
      questionText: selectedQuestion[0][0].text,
      questionType: selectedQuestion[0][0].type,
      answers: [],
      correctAnswers: selectedQuestion[0][1].map(a => a.is_correct),
      questionId: selectedQuestion[0][0].id
    };

    // Ajouter les réponses à l'objet de la question
    for (let j = 0; j < answerstemp.length; j++) {
      questionObject.answers.push({
        answer : answerstemp[j].text,
        answerId : answerstemp[j].id
      });
      if (answerstemp[j].is_correct) {
        questionObject.correctAnswers.push(j);
      }
    }

    listQuestionId.push(selectedQuestion[0][0].id);
    listAnswerId.push(selectedQuestion[0][1].map(a => a.id));

    const existingIndex = listQuestionObject.questions.findIndex(q => q.questionId === questionId);
    if (existingIndex !== -1) {
      listQuestionObject.questions.splice(existingIndex, 1, questionObject);
    } else {
      listQuestionObject.questions.push(questionObject);
    }
  }
  //trouve la position de la dernière question dans la liste de question
  const lastQuestionIndex = listQuestionObject.questions.length - 1;

  currentPageIndex.value = lastQuestionIndex;

  question.value = listQuestionObject.questions[lastQuestionIndex].questionText;
  questionType.value = listQuestionObject.questions[lastQuestionIndex].questionType;
  newAnswers.value = listQuestionObject.questions[lastQuestionIndex].answers.map(a => a.answer);
  correctAnswers.value = listQuestionObject.questions[lastQuestionIndex].correctAnswers;
  updateCheckboxes();
  selectedQuestionIds.value = [];
  currentDisplay.value = 'CancelQuestionBank';
}

function handleCheckboxClick(index) {
  if (questionType.value === 'single_answer') {
    // Pour single_answer, assurez-vous qu'une seule case à cocher est sélectionnée à la fois
    correctAnswers.value = [index];
    const checkboxes = document.querySelectorAll('.check');
    checkboxes.forEach((checkbox, i) => {
      checkbox.checked = i === index;
    });
  } else if (questionType.value === 'multiple_answers') {
    // Pour multiple_answers, basculez la sélection de la case à cocher
    const selectedIndex = correctAnswers.value.indexOf(index);
    if (selectedIndex > -1) {
      correctAnswers.value.splice(selectedIndex, 1); // Désélectionner
    } else {
      correctAnswers.value.push(index); // Sélectionner
    }
  }
}

watch(questionType, (newType, oldType) => {
  if (newType === 'single_answer' && correctAnswers.value.length > 1) {
    // Si le nouveau type est 'single_answer' et qu'il y a plusieurs réponses correctes sélectionnées,
    const firstSelectedAnswer = correctAnswers.value[0];
    correctAnswers.value = [firstSelectedAnswer];
  } else if (newType !== 'multiple_answers' && newType !== 'single_answer') {
    // Si le nouveau type n'est ni 'multiple_answers' ni 'single_answer',
    correctAnswers.value = [];
  }
  updateCheckboxes();
});
</script>


<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <div class="Page">
    <div style="margin-top: -33px; width: 100%">
      <Header />
    </div>
    <div class="top">
      <label>
        <p style="display: none">
          {{ $t("create.title") }}
          <!-- Title -->
        </p>
        <input
          v-model="surveyTitle"
          type="text"
          maxlength="25"
          :placeholder="$t('create.creaName')"
        >
      </label>
    </div>

    <div class="return">
      <button class="btnReturn">
        <img
          src="@/components/icons/return.svg"
          alt="return"
          @click="router.push('/surveys')"
        >
      </button>
    </div>

    <div class="textArea">
      <label>
        <p style="display: none">
          {{ $t("create.description")  }}
          <!-- Description -->
        </p>
        <textarea
          v-model="surveyDescription"
          :placeholder="$t('create.textArea')"
          class="textDef"
          @input="autoExpand"
        />
      </label>
    </div>

    <hr>
    <div class="nbrQst">
      <button
        :disabled="currentPageIndex.value === 0"
        @click="goToPreviousPage()"
      >
        &#10096;
      </button>
      <button @click="remvPage()">
        &#x2212;
      </button>
      <h2>{{ $t("create.question") }} </h2>
      <h2>{{ currentPageIndex + 1 }}</h2>
      <button @click="addNewPage()">
        &#10010;
      </button>
      <button
        :disabled="currentPageIndex.value === pages.length - 1"
        @click="goToNextPage()"
      >
        &#x2771;
      </button>
    </div>
    <hr>

    <div class="wrapper">
      <button
        class="importQuestion"
        @click="handleImportQuestion()"
      >
        {{ $t("create.importFrom") }}
        <!-- Import from question bank -->
      </button>

      <button
        class="delete"
        @click="deleteCurrentQuestion()"
      >
        <img
          src="@/assets/bean.svg"
          alt="delete"
        >
      </button>
    </div>

    <div 
      v-if="currentDisplay === 'QuestionBank'"
    >
      <ImportQuestion /> 
    </div>

    <div class="rectangle">
      <div class="logo">
        <select v-model="questionType"
                class="select"
        >
          <option class="option"
                  value="multiple_answers"
          >
            {{ $t("create.multipleAnswers")  }}
            <!-- multiple answers -->
          </option>
          <option class="option"
                  value="single_answer"
          >
            {{ $t("create.singleAnswer")  }}
            <!-- single answer -->
          </option>
          <option class="option"
                  value="open"
          >
            {{ $t("create.open")  }}
            <!-- open -->
          </option>
          <option class="option"
                  value="open_restricted"
          >
            {{ $t("create.openRestricted")   }}
            <!-- open restricted -->
          </option>
        </select>
      </div>

      <label>
        <p style="display: none">
          {{ $t("create.question") }}
          <!-- Question -->
        </p>
        <textarea
          v-model="question"
          maxlength="150"
          :placeholder="$t('create.text')"
          class="text areaQuestion"
          @input="autoExpand"
        />
      </label>
    </div>


    <div 
      v-if="questionType === 'multiple_answers' || questionType === 'single_answer'"
      class="answer"
    >
      <select
        v-model="selectedQuestionCount"
        class="selectNumber"
        @change="updateQuestions()"
      >
        <option
          v-for="option in questionCountOptions"
          :key="option"
          :value="option"
        >
          {{ option }}
        </option>
      </select>

      <div
        v-for="(answer, index) in newAnswers"
        :key="index"
        class="number"
      >
        <label>
          <p style="display: none">
            {{ $t("create.answer") }}
            <!-- Answer -->
          </p>
          <input
            type="text"
            :value="answer"
            class="answerSelect"
            @input="updateListAnswer($event, index)"
          >
        </label>
        <label>
          <p style="display: none">
            {{ $t("create.check") }}
            <!-- Check -->
          </p>
          <input
            type="checkbox"
            class="check"
            :checked="correctAnswers.includes(index)"
            @click="handleCheckboxClick(index)"
          >
        </label>
      </div>
    </div>

    <div class="foot">
      <div class="select">
        <select
          v-model="selectedOption"
          class="end"
        >
          <option value="save">
            {{ $t("create.save") }}
          </option>
          <option value="export">
            {{ $t("create.export") }}
          </option>
          <option value="launch">
            {{ $t("create.saveLaunch") }}
          </option>
        </select>

        <button
          v-if="selectedOption === 'save'"
          @click="saveSurvey()"
        >
          <img src="@/components/icons/save.svg"
               alt="save"
          >
        </button>
        <button v-if="selectedOption === 'export'">
          <img src="@/components/icons/dl.svg"
               alt="save and export"
          >
        </button>
        <button v-if="selectedOption === 'launch'"> 
          <img src="@/components/icons/play.svg"
               alt="launch"
          >
        </button>
      </div>
    </div>


    <gear />
  </div>
</template>
  
  
<style scoped>
* {
    font-family: 'Sofia Sans', sans-serif;
    color: var(--text-color);
}

/*
  ********************************************************************************************************
  ********************************************************************************************************
  css du main
  ********************************************************************************************************
  ********************************************************************************************************
  */

.Page {
    display: flex;
    flex-direction: column;
    margin: 2% 0 0 0;
    align-items: center;
}

button {
    background-color: transparent;
    border: none;
}

.nbrQst {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.importQuestion {
  margin-left: auto;
  margin-right: auto;
  margin-top: 1em;
  display: flex;
  border-radius: 20px;
  border: 1px solid var(--main-color);
  background-color: var(--background);
  padding: 0.5em 2em;
  text-decoration: none;
  color: var(--text-color);
  font-family: "Sofia Sans", sans-serif;
}

.importQuestion:hover {
  cursor: pointer;
  background-color: var(--main-color);
  color: var(--white);
  transition: 700ms;
}

.nbrQst button {
    cursor: pointer;
    font-size: 1.5em;
    margin: 0 70px;
}

.top input {
    font-size: 2em;
    border: none;
    border-bottom: 1px solid var(--main-color);
    background-color: transparent;
    outline: none;
    text-align: center;

}

.top {
    margin: 15px 0 5px 0;
}

.return {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    width: 90%;
    margin: 0 0 1% 0;
}

.btnReturn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    transition: 500ms;
    filter: var(--filter);
}

.btnReturn:hover {
    background-color: #17273a23;
    border-radius: 10%;
    transition: 500ms;
}

hr {
    width: 100%;
    margin: 0;
    border: 1px solid var(--CTA-color);
}

.wrapper {
    display: flex;
    flex-direction: row;
    margin-top: 30px;
    align-items: center;
    justify-content: center;
}

.wrapper p {
    font-size: 2.2em;
}

h2 {
    margin: 10px;
}

.rectangle {
    width: 70%;
    border: 1px solid var(--main-color);
    border-radius: 10px;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.logo {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: flex-start;
    transition: 300ms;
}

.filter {
    filter: invert(77%) sepia(14%) saturate(4%) hue-rotate(314deg) brightness(90%) contrast(96%);
    transition: 300ms;
}

.logo img:hover {
    cursor: pointer;
    transition: 300ms;
    filter: invert(11%) sepia(12%) saturate(90%) hue-rotate(172deg) brightness(98%) contrast(90%);
    background-color: #0000000c;
    border-radius: 30%;
}

.text {
    font-size: 1.5em;
    margin: 0 0 5% 0;
    border: none;
    background-color: transparent;
    outline: none;
    text-align: center;
    font-weight: bold;
    width: 50vw;
    resize: none;
    height: 15vh;
}

.selectNumber {
    padding: 16px 20px;
    border: 1px solid var(--main-color);
    border-radius: 30px;
    background-color: var(--white);
    width: auto;
    text-align: center;
    font-size: 1em;
    font-weight: bold;
}

.select{
    padding: 16px 20px;
    border: 1px solid var(--CTA-color);
    border-radius: 20px;
    background-color: var(--white);
    width: auto;
    text-align: center;
    font-size: 1em;
    font-weight: bold;
}

.option {
    font-size: 1em;
}

.answer {
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.number {
    display: flex;
    flex-direction: row;
}

.answerSelect {
    width: 250px;
    min-height: 40px;
    height: auto;
    border-radius: 30px;
    border-color: var(--main-color);
    border-width: 2px;
    padding-left: 20px;
    font-size: 1.2em;
    text-decoration: underline;
    background-color: var(--background);
}

.answerSelect:focus {
    border: 3px solid var(--main-color);
    outline: none;
    color: var(--text-color);
    text-decoration: none;
}

.check {
    width: 2em;
    height: 2em;
    border: 3px solid var(--main-color);
    border-radius: 30px;
    appearance: none;
    justify-content: center;
    align-items: center;
    margin: 9px 30px;
    transition: 500ms;
}

.check:hover {
    cursor: pointer;
}

.check:checked {
    background-color: var(--main-color);
}


.number {
    display: flex;
    margin: 10px;
}

.foot {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin: 60px 0;
}

.foot{
    background-color: var(--CTA-2-color);
    color: var(--white);
    border-radius: 30%;
}

.textArea {
    margin: 0 50px 20px 0;
}

.textDef {
    width: 70vw;
    height: 50px;
    padding: 12px 20px;
    box-sizing: border-box;
    border: 2px solid var(--main-color);
    border-radius: 25px;
    resize: none;
    font-size: 1em;
    background-color: var(--background);
}

.delete {
  margin-left: 20px;
  background: var(--CTA-2-color);
  width: 80px;
  height: 45px;
  padding: 5px;
  cursor: pointer;
  transition: 500ms;
  border-radius: 30px;
}

.delete:hover {
    background: var(--CTA-2-hover-color);
    border-radius: 30px;
}


.select {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.select img {
    cursor: pointer;
    width: 35px;
    height: 35px;
    padding: 3px;
    margin: 0 10px;
    border-radius: 45%;
    filter: var(--filter);
}

.end {
    margin-left: 50px;
    width: auto;
    height: 40px;
    border: 2px solid var(--main-color);
    font-size: 18px;
    color: var(--text-color);
    background-color: var(--white);
    border-radius: 25px;
    text-align-last: center;
}

/*
  ********************************************************************************************************
  ********************************************************************************************************
  css responsive
  ********************************************************************************************************
  ********************************************************************************************************
*/

@media screen and (max-width: 1000px) {

    .rectangle {
        width: 90%;
    }

    .nbrQst button {
        font-size: 1.5em;
        margin: 0 50px;
    }
}

@media screen and (max-width: 700px) {

    .Page {
        margin: 5% 0 0 0;
    }

    .top {
        font-size: 0.8em;
    }

    .nbrQst button {
        font-size: 1.5em;
        margin: 0 15px;
    }

    .nbrQst h2 {
        font-size: 1.2em;
    }

    .answerSelect {
        width: 200px;
    }

    .foot {
        display: flex;
        flex-direction: column;
    }

    .delete {
        margin-bottom: 20px;
    }
}

.areaQuestion {
  width: 35vw;
  min-height: 45px;
  resize: none;
  overflow: hidden;
  padding: 5% 5%;
  box-sizing: border-box;
}
</style>