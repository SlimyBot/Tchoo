<script setup>
// Coté étudiant
import { ref } from "vue";

import Gear from "@/components/Gear.vue";
import Header from "@/components/Header.vue";
import Timer from "@/components/Timer.vue";

const props = defineProps({ isRestricted: { type: Boolean, default: false } })

const emits = defineEmits(["answer"])

const openAnswerText = ref("");

function openAnswerValid() {
  return !props.isRestricted || !(openAnswerText.value.split(" ").length > 1)
}

function submitOpenAnswer() {
  emits("answer", openAnswerText.value)
}
</script>


<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <Header />

  <main>
    <div class="bloc">
      <input v-model="openAnswerText"
             type="text"
             :placeholder="$t('freeAnsw.placeholder')"
      >
      <!-- <input v-model="openAnswerText"
             type="text"
             placeholder="Votre réponse"
      > -->

      <button :disabled="openAnswerText === '' || !openAnswerValid()"
              @click="submitOpenAnswer()"
      >
        <span class="material-symbols-outlined"> arrow_forward </span>
      </button>
    </div>
    <Gear />
    <!-- Timer désactivé pour l'instant -->
    <!-- <div class="timer">
      <Timer nb="1" time="∞" />
    </div> -->
  </main>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Sofia+Sans:wght@300&display=swap");


@media screen and (max-width: 800px) {
  .divHeader {
    width: 90%;
  }
}

main {
  display: flex;
  align-items: center;
  background-image: url("../../icons/BG_OPEN_ANSWER.png");
  background-size: cover;
  background-position: center;
  width: 98vw;
  height: 88vh;
}

.bloc {
  margin-left: auto;
  margin-right: auto;
  display: block;
}

input {
  display: block;
  margin-left: auto;
  margin-right: auto;
  border-radius: 30px;
  height: 5vh;
  width: 50vw;
  padding: 20px;

  border: var(--CTA-color) 2px solid;

  font-size: 20px;
  font-family: "Sofia Sans", sans-serif;
}

button {
  display: block;
  padding: 12px 100px;
  border-radius: 50px;
  background-color: var(--CTA-color);
  border: none;
  cursor: pointer;
  margin-right: auto;
  margin-left: auto;
  margin-top: 20px;
}

button:disabled {
  cursor: not-allowed;
  background-color: grey;
}

.material-symbols-outlined {
  font-variation-settings: "FILL" 0, "wght" 300, "GRAD" 0, "opsz" 24;
  color: var(--white);
}
</style>
