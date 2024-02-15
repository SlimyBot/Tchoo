<script setup>
// Coté prof
import openStore from "@/lib/openAnswersStore"
import Gear from "@/components/Gear.vue";

import Timer from "@/components/Timer.vue";
import Question from "@/components/question/Question.vue";

/* eslint-disable */
const props = defineProps({
  question: { type: Object, required: true },
  isRestricted: { type: Boolean, required: true }
})
/* eslint-enable */
</script>

<template>
  <main>
    <div class="question">
      <Question :question="props.question.text" />

      <p v-if="props.isRestricted">
        {{ $t("openQst.word") }}
        <!-- Un seul mot autorisé -->
      </p>

      <div class="open-answers">
        <TransitionGroup name="opens">
          <div v-for="answer in openStore.openAnswers"
               :key="answer"
               class="open-answer"
          >
            {{ answer }}
          </div>
        </TransitionGroup>
      </div>

      <!-- TODO : désactivé pour l'instant -->
      <!-- <div class="timer">
        <Timer />
      </div> -->
    </div>
  </main>
  <Gear />
</template>


<style scoped>
.open-answers {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1em;
  padding-inline: 2em;
  padding-bottom: 2em;
}

.open-answer {
  border: 1px dashed #130f0f;
  padding: 1em;
  border-radius: 10px;
  background-color: white;
}

.opens-move,
.opens-enter-active,
.opens-leave-active {
  transition: all 0.5s ease;
}

.opens-enter-from,
.opens-leave-to {
  opacity: 0;
  transform: scaleY(0.01) translateX(30px);
}

.opens-leave-active {
  position: absolute;
}

main {
  background-image: url("../../icons/BG_OPEN_QUESTION.png");
  background-position: center;
  background-size: cover;
  width: 98vw;
  height: 85vh;

  text-align: center;
}

.bloc {
  display: block;
  position: absolute;
  margin-left: auto;
  margin-right: auto;

  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  border-radius: 30px;
  height: 10vh;
  width: 50vw;
  padding-top: 5vh;
  text-align: center;

  border: var(--CTA-color) 2px solid;
  color: var(--text-color);

  font-size: 20px;
  font-family: "Sofia Sans", sans-serif;
}

.question {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  gap: 1.5em;
}

* {
  font-family: "Sofia Sans", sans-serif;
}
</style>