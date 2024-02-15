<script setup>
import { ref } from 'vue';

const emit = defineEmits(["showResults", "pauseAnswers", "nextQuestion", "stopSession"])

const showResultsState = ref(false)
const acceptingAnswersState = ref(true)

function showResults() {
  showResultsState.value = !showResultsState.value
  emit("showResults", showResultsState.value)
}

function pauseAnswers() {
  acceptingAnswersState.value = !acceptingAnswersState.value
  emit("pauseAnswers", acceptingAnswersState.value)
}

function nextQuestion() {
  emit("nextQuestion")
}

function stopSession() {
  emit("stopSession")
}
</script>

<template>
  <div class="centered-menu">
    <div class="menu">
      <!--
      <button class="see"
              disabled
              @click="showResults()"
      >
        <img src="@/assets/Eye.png"
             alt="Menu"
             :class="showResultsState ? 'grayscale' : ''"
        >
      </button>
      <button class="pause"
              disabled
              @click="pauseAnswers()"
      >
        <img v-if="acceptingAnswersState"
             src="@/assets/Pause.png"
             alt="Menu"
        >
        <img v-else
             src="@/assets/Play.png"
             alt="Menu"
        >
      </button>
      -->
      <button class="forward"
              @click="nextQuestion()"
      >
        <img src="@/assets/Forward.png"
             alt="Menu"
        >
      </button>
      <button class="stop"
              @click="stopSession()"
      >
        <img src="@/assets/Stop.png"
             alt="Menu"
             style="width: 18px; height: 20px;"
        >
      </button>
    </div>
  </div>
</template>

<style scoped>
.centered-menu {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.menu {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 250px;
  height: 50px;
  border-radius: 50px;
  background-color: transparent;
  overflow: hidden;
  margin: 20px;
}

.menu button {
  border-radius: 20px;
  border: 1px solid var(--main-color);
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
}

button:disabled:hover {
  cursor: not-allowed;
}

.menu button img {
  max-width: 100%;
  max-height: 100%;
  transition: opacity 200ms;
}

.grayscale {
  opacity: 0.5;
}

.see {
  width: 40px;
  height: 30px;
}

.eye {
  width: 20px;
  height: 20px;
}

.backward {
  width: 55px;
  height: 40px;
}

.pause {
  width: 70px;
  height: 45px;
}

.forward {
  background-color: transparent;
  padding: 10px;
  width: 100px;
  height: 50px;
  opacity: 1;

  filter: var(--filter);
}

.stop {
  background-color: transparent;
  padding: 10px;
  width: 100px;
  height: 50px;

  filter: var(--filter);
}
</style>
