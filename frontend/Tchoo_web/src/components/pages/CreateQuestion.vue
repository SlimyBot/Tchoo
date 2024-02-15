<script setup>
import { ref, onMounted, nextTick } from 'vue';
import Gear from "@/components/Gear.vue";
import { useRouter, useRoute } from "vue-router";
import {
  createAnswer, getQuestion, updateQuestion,
  updateAnswer, deleteAnswer, removeQuestion
} from '../../lib/requests.js';
import Header from "@/components/Header.vue";

const router = useRouter();
const route = useRoute();
const questionId = route.params.id;
const newAnswers = ref(['']);
const correctAnswers = ref([]);
const selectedOption = ref('save');
const questionText = ref("");
const questionType = ref('multiple_answers');
const selectedQuestionCount = ref(1);
const questionCountOptions = [1, 2, 3, 4, 5, 6, 7, 8];
const answersId = [];

onMounted(async () => {
  await importQuestion();
});

async function importQuestion() {
  let question = await getQuestion(questionId);
  questionText.value = question[0][0].text;
  questionType.value = question[0][0].type;
  if (question[0][1].length > 0){
    newAnswers.value = question[0][1].map(answer => answer.text);
    question[0][1].forEach(answer => answersId.push(answer.id));
    for (let i = 0; i < question[0][1].length; i++) {
      if (question[0][1][i].is_correct)
        correctAnswers.value.push(i);
    }
    updateCheckboxes();
  }
}

function updateCheckboxes() {
  if (newAnswers.value.length > 0) {
    selectedQuestionCount.value = newAnswers.value.length;

    nextTick(() => {
      requestAnimationFrame(() => {
        const checkboxes = document.querySelectorAll('.check');
        checkboxes.forEach((checkbox, index) => {
          checkbox.checked = correctAnswers.value.includes(index);
        });
      });
    });
  }
  else {
    selectedQuestionCount.value = 1;
  }
}

async function updateQuest() {
  await updateQuestion(questionId, questionText.value, "none", questionType.value);
  const answerElements = document.querySelectorAll('.check');
  for (let i = 0; i < newAnswers.value.length; i++) {
    if ( i >= answersId.length){
      await createAnswer(questionId, newAnswers.value[i], answerElements[i].checked);
    }else{
      await updateAnswer(answersId[i], newAnswers.value[i], answerElements[i].checked);
    } 
  }
  router.push('/surveys');
}

async function updateQuestions() {
  const currentLength = newAnswers.value.length;
  const newLength = selectedQuestionCount.value;

  if (newLength > currentLength) {
    for (let i = currentLength; i < newLength; i++) {
      newAnswers.value.push('');
    }
  } else if (newLength < currentLength) {
    for (let i = currentLength; i > newLength; i--) {
      if(answersId[i - 1]!==undefined){ 
        await deleteAnswer(answersId[i - 1]);
      }
    }
    newAnswers.value = newAnswers.value.slice(0, newLength);
  }
};

async function deleteQuestion() {
  await removeQuestion(questionId);
  router.push('/surveys');
}

function updateListAnswer(event, index) {
  newAnswers.value[index] = event.target.value;
}

function autoExpand(event) {
  event.target.style.height = 'inherit';
  event.target.style.height = `${event.target.scrollHeight}px`;
}


</script>

<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <Header />

  <div class="Page">
    <div class="return">
      <button class="btnReturn">
        <img src="@/components/icons/return.svg"
             alt="return"
             @click="router.push('/surveys')"
        >
      </button>
    </div>

    <div class="wrapper">
      <button class="delete"
              @click="deleteQuestion()"
      >
        <img src="@/assets/bean.svg"
             alt="delete"
        >
        <p style="display: none">
          Return
        </p>
      </button>
    </div>

    <div class="rectangle">
      <div class="logo">
        <select v-model="questionType"
                class="select"
        >
          <option class="option"
                  value="multiple_answers"
          >
            {{ $t("createQst.multiple") }}
            <!-- multiple answers -->
          </option>
          <option class="option"
                  value="single_answer"
          >
            {{ $t("createQst.single") }}
            <!-- single answer -->
          </option>
          <option class="option"
                  value="open"
          >
            open
          </option>
          <option class="option"
                  value="open_restricted"
          >
            {{ $t("createQst.openRestricted")  }}
            <!-- open restricted -->
          </option>
        </select>
      </div>
      <label>
        <p style="display: none">Question</p>
        <textarea
          v-model="questionText"
          :placeholder="$t('create.text')"
          class="text"
          @input="autoExpand"
        />
      </label>
    </div>


    <div 
      v-if="questionType === 'multiple_answers' || questionType === 'single_answer'"
      class="answer"
    >
      <label>
        <p style="display: none">Number of answers</p>
        <select v-model="selectedQuestionCount"
                class="selectNumber"
                @change="updateQuestions()"
        >
          <option v-for="option in questionCountOptions"
                  :key="option"
                  :value="option"
          >
            {{ option }}
          </option>
        </select>
      </label>

      <div v-for="(answer, index) in newAnswers"
           :key="index"
           class="number"
      >
        <label>
          <p style="display: none">Answer</p>
          <input type="text"
                 :value="answer"
                 class="answerSelect"
                 @input="updateListAnswer($event, index)"
          >
        </label>
        <label>
          <p style="display: none">Checkbox</p>
          <input type="checkbox"
                 class="check"
          >
        </label>
      </div>
    </div>

    <div class="foot">
      <div class="select">
        <label>
          <p style="display: none">Select option</p>
          <select v-model="selectedOption"
                  class="end"
          >
            <option value="save">
              {{ $t("create.save") }}
            </option>
            <option value="export">
              {{ $t("create.export") }}
            </option>
          </select>
        </label>

        <button v-if="selectedOption === 'save'"
                @click="updateQuest()"
        >
          <img src="@/components/icons/save.svg"
               alt="Save"
          >
        </button>
        <button v-if="selectedOption === 'export'">
          <img src="@/components/icons/dl.svg"
               alt="Export"
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

.Page {
    display: flex;
    flex-direction: column;
    margin: 2% 0 0 0;
    align-items: center;
}

.text {
  font-size: 1em;
  border: none;
  background-color: transparent;
  outline: none;
  text-align: center;
  width: 40vw;
  resize: none;
  height: 10vh;
}

button {
    background-color: transparent;
    border: none;
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
    border-radius: 10%;
    transition: 500ms;
}

.wrapper {
    display: flex;
    flex-direction: row;
    margin-top: 30px;
    align-items: center;
    justify-content: center;
}

.number {
    display: flex;
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

.select{
    padding: 16px 20px;
    border: none;
    border-radius: 30px;
    background-color: var(--white);
    width: auto;
    text-align: center;
    font-size: 1em;
    font-weight: bold;
}

div .select {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.option {
    font-size: 1em;
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
    border-bottom: 1px solid var(--main-color);
    background-color: transparent;
    outline: none;
    font-weight: bold;
}

.selectNumber {
    padding: 16px 20px;
    border: var(--main-color) 1px solid;
    border-radius: 30px;
    background-color: var(--white);
    width: auto;
    text-align: center;
    font-size: 1em;
    font-weight: bold;
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
    border-radius: 20px;
    border-color: var(--main-color);
    background-color: var(--background);
    border-width: 2px;
    padding-left: 20px;
    font-size: 1.2em;
    text-decoration: underline;
}

.answerSelect:focus {
    border: 3px solid var(--CTA-color);
    outline: none;
    color: var(--text-color);
    text-decoration: none;
}

.check {
    width: 2em;
    height: 2em;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    appearance: none;
    justify-content: center;
    align-items: center;
    margin: 8px 30px
}

.check :hover {
    cursor: pointer;
}

.check:checked {
    background-color: var(--main-color);
}

.foot {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin: 60px 0;
}

.delete img {
    background: var(--CTA-2-color);
    width: 90px;
    height: 20px;
    padding: 10px;
    cursor: pointer;
    transition: 500ms;
    border-radius: 30px;
}

.delete img:hover {
    background: var(--CTA-2-hover-color);
    border-radius: 30px;
}

.delete img:active {
    background: var(--black);
    border-radius: 30%;
    transition: 100ms;
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
    border: 2px solid var(--CTA-color);
    transition: 500ms;
    filter: var(--filter);
}

.end {
    width: 10rem;
    height: 45px;
    border: 2px solid var(--main-color);
    font-size: 18px;
    color: var(--text-color);
    background-color: var(--white);
    border-radius: 25px;
    text-align-last: center;
    margin-left: -10px;
}

@media screen and (max-width: 1000px) {
    .rectangle {
        width: 90%;
    }
}

@media screen and (max-width: 700px) {
    .Page {
        margin: 5% 0 0 0;
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
    max-width: 35vw;
    min-height: 45px;
    resize: none;
    overflow: hidden;
    padding: 5% 5%;
    box-sizing: border-box;
}
</style>