<script setup>
import { getAllSurveySessions } from "@/lib/requests.js"
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

import Header from "@/components/Header.vue";
import {useRouter} from "vue-router";
import Gear from "@/components/Gear.vue"
import ClearButton from "@/components/ClearButton.vue";

const router = useRouter();
const sessions = ref({});
const route = useRoute();

async function onFormSubmit() {
  let statusCode;
  let json;
  [json, statusCode] = await getAllSurveySessions();
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

function formatDate(dateString) {
  const date = new Date(dateString);
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}

</script>

<template>
  <Header />
  <body>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
    >
    <div class="return">
      <button class="btnReturn">
        <img
          src="@/components/icons/return.svg"
          alt="return"
          @click="router.push('/Surveys')"
        >
      </button>
    </div>
    <div class="top">
      <h1>
        {{ $t("session.history") }}
        <!-- Historique des sessions -->
      </h1>
      <ClearButton to="/results" >
        {{ $t("session.results") }}
        <!-- Résultats -->
      </ClearButton>
    </div>
    <hr>
    
    <div class="bentoGrid">
      <div v-for="session in sessions"
           :key="session.join_code"
           class="surveyRes"
      >
        <div v-if="session.finished === true">
          <router-link :to="'/endSurvey/' + session.join_code"
                       class="router"
          >
            <p class="nameP">
              {{ session.name }}
            </p>
            <p class="finished">
              {{ $t("session.finished") }}
              <!-- État : Terminée -->
            </p>
            <p class="joinCode">
              {{ $t("session.joinCode")  }}:
              <!-- Code Session :  -->
              {{ session.join_code }}
            </p>
            <p class="createdDate">
              {{ formatDate(session.created_at) }}
            </p>  
          </router-link>
        </div>
        <div v-else>
          <p class="nameP">
            {{ session.name }}
          </p>
          <p class="finished">
            {{ $t("session.inProgress") }}
            <!-- État : En cours -->
          </p>
          <p class="joinCode">
            {{ $t("session.joinCode")  }}:
            <!-- Code Session :  -->
            {{ session.join_code }}
          </p>
          <p class="createdDate">
            {{ formatDate(session.created_at) }}
          </p>
        </div>
      </div>
    </div>
    <Gear />
  </body>
</template>

<style>

* {
  font-family: 'Sofia Sans', sans-serif;
  color: var(--text-color);
}

body {
  width: 96vw;
}

.material-symbols-outlined {
  font-variation-settings:
      'FILL' 0,
      'wght' 400,
      'GRAD' 0,
      'opsz' 24
}

.top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 2% 0 0 0;
}

hr {
  border: none;
  height: 1px;
  width: 90%;
  background-color: var(--text-color);
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
  border-radius: 30px;
  transition: 500ms;
}

.bentoGrid {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 30px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.surveyRes {
  background-color: var(--background);
  border: solid 1px var(--main-color);
  border-radius: 10px;
  padding: 15px;
  padding-left: 25px;
  width: 30%;
  transition: 0.15s ease-in-out;
}

.surveyRes:hover {
  background-color: var(--CTA-color);
  color: white;

  transition: 0.3s ease-in-out;
}

.surveyRes:hover p {
  color: white;
}

.nameP {
  text-decoration: none;
  text-align: center;
  margin: auto;
  font-weight: 600;
  margin-top: 5px;
  font-size: 20px;
}

.createdDate{
  text-align: right;
  margin-right: 10px;
}

.finished{
  margin-top: 15px;
  margin-bottom: -10px;
}

a {
  text-decoration: none;
}


</style>