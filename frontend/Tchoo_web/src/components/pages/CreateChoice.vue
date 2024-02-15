<script setup>
import { ref, computed } from 'vue';

const pages = ref([{ question: 'Question texte', time: 60 }]);
const currentPageIndex = ref(0);

const formattedTime = computed(() => {
  const minutes = Math.floor(pages.value[currentPageIndex.value].time / 60);
  const seconds = pages.value[currentPageIndex.value].time % 60;
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
});

const incrementTime = () => {
  if (pages.value[currentPageIndex.value].time < 120) {
    pages.value[currentPageIndex.value].time += 15;
  }
};

const decrementTime = () => {
  if (pages.value[currentPageIndex.value].time > 15) {
    pages.value[currentPageIndex.value].time -= 15;
  }
};

const updateQuestions = () => {
  // Réinitialisez les questions si le nombre de questions change
};


const remvPage = () => {
  if (pages.value.length > 1) {
    pages.value.pop();
        
    if (currentPageIndex.value >= pages.value.length) {
      currentPageIndex.value = pages.value.length - 1;
    }
  }
};

const addNewPage = () => {
  pages.value.push({ question: 'Question texte', time: 60 });
  currentPageIndex.value = pages.value.length - 1;
};

const goToPreviousPage = () => {
  if (currentPageIndex.value > 0) {
    currentPageIndex.value--;
  }
};

const goToNextPage = () => {
  if (currentPageIndex.value < pages.value.length - 1) {
    currentPageIndex.value++;
  }
};

const selectedOption = ref('save');

const time = formattedTime;

const selectedQuestionCount = ref(1);
const questionCountOptions = [1, 2, 3, 4, 5, 6, 7, 8];

const changeLanguage = (lang) => {
  this.$i18n.locale = lang;
  this.closeMenu();
};

import Gear from "@/components/Gear.vue";
import Header from "@/components/Header.vue";


const components = {
  Gear,
  Header
};


</script>



<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <div class="Page">
    <div class="top">
      <p
        contentEditable="true"
        onkeypress="return (this.innerText.length <= 25)"
      >
        {{ $t("create.creaName") }}
      </p>
    </div>

    <hr>
    <div class="nbrQst">
      <button
        :disabled="currentPageIndex.value === 0"
        @click="goToPreviousPage"
      >
        &#10096;
      </button>
      <button @click="remvPage">
        &#x2212;
      </button>
      <h2>{{ $t("create.question") }} </h2>
      <h2>{{ currentPageIndex + 1 }}</h2>
      <button @click="addNewPage">
        &#10010;
      </button>
      <button
        :disabled="currentPageIndex.value === pages.length - 1"
        @click="goToNextPage"
      >
        &#x2771;
      </button>
    </div>
    <hr>

    <div class="choose">
      <button> {{ $t("create.open") }}</button>
      <button> {{ $t("create.multiple") }}</button>
      <button> {{ $t("create.import") }}</button>
      <button> {{ $t("create.importMany") }}</button>
    </div>

    <gear />
  </div>
</template>
  
  
<style scoped>
* {
    font-family: 'Sofia Sans', sans-serif;
    color: #17273A;
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
    margin: 5% 0 0 0;
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

.nbrQst button {
    cursor: pointer;    
    font-size: 1.5em;
    margin: 0 70px;}

p {
    font-size: 2em;
    margin: 0;
}

.top {
    margin-bottom: 40px;
}

hr {
    width: 80%;
    margin: 0;
    border: 1px solid var(--CTA-color);
}

h2 {
    margin: 10px;
}

.choose{
    display: flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
    margin: 50px 0;
}

.choose button{
    width: 400px;
    height: 50px;
    border-radius: 25px;
    border: 2px solid var(--CTA-color);
    background-color: var(--white);
    font-size: 18px;
    color: var(--text-color);
    margin: 20px;
    cursor: pointer;
}

.choose button:hover{
    background-color: var(--CTA-color);
    color: var(--white);
    transition: 700ms;
    border-color: var(--white);
    border: 2px solid var(--white);
}

.material-symbols-outlined {
    font-variation-settings:
        'FILL' 0,
        'wght' 150,
        'GRAD' 0,
        'opsz' 24;
    font-size: 55px;
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

    .nbrQst button {
        font-size: 1.5em;
        margin: 0 15px;
    }

    .choose button {
        width: 350px;
    }

}
</style>
  
  