<script setup>
import { getSessionsPlayer } from "@/lib/requests.js"
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Header from "@/components/Header.vue";
import Gear from "@/components/Gear.vue";
import router from "@/lib/router.js";
import {isTeacher} from "@/lib/auth.js";

const sessions = ref({});
const route = useRoute();
var jsonObject = ref({});
var test = ref({})

async function onFormSubmit() {
  let statusCode;
  let json;
  [json, statusCode] = await getSessionsPlayer();
  if (statusCode !== 200) {
    alert(json.detail);
    return
  }
  sessions.value = json;
  console.log(sessions.value);

}

onMounted(async () => {
  await onFormSubmit();
});

</script>

<template>
  <Header />
  <button v-if="isTeacher()"
          class="btnReturn"
  >
    <img
      src="@/components/icons/return.svg"
      alt="return"
      @click="router.push('/AllSessions')"
    >
  </button>
  <div class="topMenu">
    <h2>
      {{ $t ("student.res") }}
      <!-- Vos résultats disponibles -->
    </h2>
    <span />
  </div>

  <div class="bentoGrid">
    <div v-for="session in sessions"
         :key="session.join_code"
         class="surveyRes"
    >
      <router-link :to="'/endSurvey/' + session.id_player + '/' + session.join_code"
                   class="router"
      >
        <p class="nameP">
          {{ session.survey_title }}
        </p>
        <p class="authorP">
          {{ session.owner_name }}
        </p>
        <div class="scoreP">
          <div v-if="session.total_answers !== 0 && session.total_open_answers !== 0">
            Score : {{ session.correct_answers }}/{{ session.total_answers }} <br>
            {{ $t("student.open") }}:
            <!-- Questions ouvertes :  -->
            {{ session.total_open_answers }}
          </div>
          <div v-else-if="session.total_answers !== 0">
            {{ $t("student.score") }} :
            <!-- Score :  -->
            {{ session.correct_answers }}/{{ session.total_answers }}
          </div>
          <div v-else-if="session.total_open_answers !== 0 ">
            {{ $t("student.open") }} :
            <!-- Questions ouvertes : -->
            {{ session.total_open_answers }}
          </div>
        </div>
      </router-link>
    </div>
  </div>
  <Gear />
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Sofia+Sans:wght@200&display=swap');

p,
h2 {
  font-family: 'Sofia Sans', sans-serif;
}

p {
  margin: 0;
  padding: 0;
}

h2 {
  font-weight: normal;
}

.topMenu {
  display: flex;
  gap: 20px;
  margin-left: 10px;
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
  border-radius: 30px;
  transition: 500ms;
}

.router {
  text-decoration: none;
}

.bentoGrid {
  margin-left: 10px;
  margin-right: 10px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.surveyRes {
  background-color: #f6f6f6;
  border-radius: 10px;
  padding: 15px;
  width: 30%;
  transition: 0.15s ease-in-out;
}

.surveyRes>.nameP,
.authorP,
.dateP {
  padding-left: 2%;
}

.nameP {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 3px;
  margin-top: 5px;
  padding-left: 10px;

  @media screen and (max-width: 450px) {
    font-size: 15px;
  }
}

span {
  width: 75%;
  height: 1px;
  margin: auto auto auto auto;
}

.scoreP {
  text-align: right;
  font-size: 25px;
  padding-right: 10px;
  font-weight: 700;
  font-family: 'Sofia Sans', sans-serif;
}

.surveyRes:hover {
  background-color: #e3e3e3;
  box-shadow: 5px 5px 20px -10px rgba(79, 112, 164, 0.4);
  width: 30.5%;

  transition: 0.3s ease-in-out;

}
</style>