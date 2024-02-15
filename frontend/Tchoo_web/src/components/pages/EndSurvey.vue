<script setup>
import { getEndSurvey } from "@/lib/requests.js"
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import PlayerResults from "@/components/finalResults/PlayerResults.vue";
import Header from "@/components/Header.vue";
import ClearButton from "@/components/ClearButton.vue";
import Gear from "@/components/Gear.vue";

const top3 = ref({})
const route = useRoute();
const showRegister = ref(false);
const join_code = route.params.join_code;

onMounted(async () => {
  let statusCode;
  let json;
  [json, statusCode] = await getEndSurvey(join_code);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  console.log(json);


  top3.value = json;
  console.log(top3);

})
</script>

<template>
  <Header/>
  <div class="container">
    <div v-if="top3 == 'Aucun resultat'"
         class="noResult"
    >
      <h3>
        {{ $t("end.noRes") }}
        <!-- Aucun résultat... -->
      </h3>
    </div>
    <div v-else>
      <div class="section">
        <div class="image-container">
          <img v-if="top3[1]"
               src="../../assets/secondTrain.png"
               alt="Image2"
               class="train2"
          >
          <img v-if="top3[1]"
               src="../../assets/rails.png"
               alt="rails"
               class="rails"
          >
        </div>
        <div v-if="top3[1]"
             class="text"
        >
          <span class="spanBold silver">{{ top3[1].name }}</span><span class="spanRow silver">{{ top3[1].correctly_answered }}
            pts</span>
        </div>
      </div>

      <div class="section">
        <div class="image-container">
          <img v-if="top3[0]"
               src="../../assets/firstTrain.png"
               alt="Image1"
               class="train1"
          >
          <img v-if="top3[0]"
               src="../../assets/rails.png"
               alt="rails"
               class="rails"
          >
        </div>
        <div v-if="top3[0]"
             class="text"
        >
          <span class="spanBold gold">{{ top3[0].name }}</span><span class="spanRow gold">{{ top3[0].correctly_answered }}
            pts</span>
        </div>
      </div>

      <div class="section">
        <div class="image-container">
          <img v-if="top3[2]"
               src="../../assets/thirdTrain.png"
               alt="Image3"
               class="train3"
          >
          <img v-if="top3[2]"
               src="../../assets/rails.png"
               alt="rails"
               class="rails"
          >
        </div>
        <div v-if="top3[2]"
             class="text"
        >
          <span class="spanBold bronze">{{ top3[2].name }}</span><span class="spanRow bronze">{{ top3[2].correctly_answered }}
            pts</span>
        </div>
      </div>

      <div class="container">
        <button class="buttonResult"
                @click="showRegister = !showRegister"
        >
          {{ $t("end.fullRes")  }}
          <!-- Résultats complets -->
        </button>
      </div>

      <div class="center-container">
        <div v-show="showRegister">
          <div v-for="(answer, index) in top3"
               :key="index"
          >
            <router-link :to="'/endSurvey/' + answer.id_player + '/' + join_code"
                         class="router"
            >
              <PlayerResults :player-name="answer.name"
                             :ranking="index + 1"
                             :score="answer.correctly_answered"
              />
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="back">
    <ClearButton to="/surveys">
      {{ $t("end.back") }}
      <!-- Retour à la page d'accueil -->
    </ClearButton>
  </div>
  <Gear />
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Sofia+Sans:wght@200&display=swap');

.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  align-content: center;
  height: auto;
  margin: auto;
}

.center-container {
  align-content: center;
  height: auto;
  margin: auto auto 15px;
}

.section {
  text-align: center;
  padding-left: 8px;
  padding-right: 8px;
  display: inline-block;
}

.image-container {
  position: relative;
  display: inline-block;
  margin-bottom: 10px;
}

.image-container img {
  max-width: 85%;
  height: auto;
  display: block;
  margin: auto;
}

.text {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
  padding: 20px;
  text-shadow: 1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000,
  1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000;
  border-radius: 30px;
}

.train1 {
  width: 100%;
}

.train2 {
  width: 65%;
}

.train3 {
  width: 55%;
}

.rails {
  width: 80%;
}

.spanRow {
  display: block;
  font-family: 'Sofia Sans', sans-serif;
  font-size: 2em;
}

.spanBold {
  font-family: "Rubik Mono One", sans-serif;
  font-size: 3em;
}

.silver {
  color: #aaaaaa;
}

.gold {
  color: #FFC738;
}

.bronze {
  color: #C2714F;
}

.container button {
  background: none;
  color: var(--text-color);
  font-size: 18px;
  margin-left: -150px;
  margin-right: -150px;
  margin-top: 2vh;
  font-family: "Sofia Sans", sans-serif;
  font-weight: bold;
  cursor: pointer;
  border: solid 1px var(--main-color);
  transition: 200ms linear;
  border-radius: 20px;
  padding: 10px 15px 10px 15px;
}

.container button:hover{
  background-color: var(--main-color);
  color: white;
}

.container p {
  color: #B5B5B5;
  padding-bottom: 10px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.wrapper {
  width: 250px;
  display: flex;
  flex-direction: row;
  justify-content: right;
  align-items: center;
  gap: 30px;
}

.router {
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  text-align: center;
}

.buttonResult {
  z-index: 3;
  background-color: white;
}

.noResult {
  text-align: center;
  align-items: center;
  font-size: 18px;
  margin-top: 100px;
  font-family: "Sofia Sans", sans-serif;
  font-weight: bold;
}

.back {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

</style>