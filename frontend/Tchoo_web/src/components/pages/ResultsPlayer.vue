<script setup>
import { getPlayerDetails } from "@/lib/requests.js"
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import PlayerResultQuestionTrue from "@/components/finalResults/PlayerResultQuestionTrue.vue";
import PlayerResultQuestionFalse from "@/components/finalResults/PlayerResultQuestionFalse.vue";
import PlayerResutlQuestionOpen from "@/components/finalResults/PlayerResultQuestionOpen.vue";
import Header from "@/components/Header.vue";
import router from "@/lib/router.js";

const infoPlayer = ref({})
const route = useRoute();
const id_player = route.params.id_player;
const join_code = route.params.join_code;

onMounted(async () => {
  let statusCode;
  let json;
  [json, statusCode] = await getPlayerDetails(id_player, join_code);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  
  

  infoPlayer.value = json;

})
</script>

<template>
  <Header />
  <div class="return">
    <button class="btnReturn">
      <img
        src="@/components/icons/return.svg"
        alt="return"
        onclick="history.go(-1);"
      >
    </button>
  </div>
  <h1>{{ infoPlayer.name }}</h1>
  <div class="center-container">
    <div v-for="(question, index) in infoPlayer.questions_answers"
         :key="index"
    >
      <div v-if="question.correctly_answered === false"
           class="centered-component"
      >
        <PlayerResultQuestionFalse :question-number="index + 1"
                                   :question="question.question_text"
                                   :answer="question.answers_text"
        />
      </div>

      <div v-else-if="question.correctly_answered === true"
           class="centered-component"
      >
        <PlayerResultQuestionTrue :question-number="index + 1"
                                  :question="question.question_text"
                                  :answer="question.answers_text"
        />
      </div>
      <div v-else
           class="centered-component"
      >
        <PlayerResutlQuestionOpen :question-number="index + 1"
                                  :question="question.question_text"
                                  :answer="question.answers_text"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Sofia+Sans:wght@200&display=swap');

h1 {
  font-family: 'Sofia Sans', sans-serif;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.center-container {
  justify-content: space-around;
  align-items: center;
  align-content: center;
  width: 70%;
  height: auto;
  margin: auto;
}

.centered-component {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 5%;
}

.btnReturn {
  background-color: transparent;
  border: none;
  border-radius: 100%;
  cursor: pointer;
  transition: 500ms;

  margin-left: 50px;
  margin-top: 50px;
  margin-bottom: -20px;
}

.btnReturn:hover {
  background-color: #17273a23;
  border-radius: 10px;
  transition: 500ms;
}


.material-symbols-outlined {
  font-variation-settings:
      'FILL' 0,
      'wght' 400,
      'GRAD' 0,
      'opsz' 24
}
</style>