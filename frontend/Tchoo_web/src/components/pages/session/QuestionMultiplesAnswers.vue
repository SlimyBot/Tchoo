<!-- 
  Page que le prof voit lors d'une session.
 -->

<script setup>
import { computed } from "vue";
import Question from "../../question/Question.vue";
import Gear from "@/components/Gear.vue";

import Timer from "../../Timer.vue";

const props = defineProps({
  /* eslint-disable */
  question: {
    type: Object,
    required: true,
  },
  /* eslint-enable */
  answers: {
    type: Array,
    required: true,
  },
});

const sortedAnswers = computed(() => {return [...props.answers].sort((a, b) => a.id - b.id)})
</script>

<template>
  <div class="outer-container">
    <div class="main-container">
      <!-- <Timer :nb="'8'" :time="'1200'" /> Timer désactivé pour l'instant -->
      <Question :question="props.question.text" />

      <div class="answer-section">
        <div class="grid-container">
          <div
            v-for="(answer, index) in sortedAnswers"
            :key="answer.id"
            class="answer-box"
          >
            <img
              src="@/components/icons/ArrowButton.svg"
              :alt="'arrow' + index"
              :class="'arrow arrow-' + index"
            >
            <p style="display: block">
              {{ answer.text }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Gear />
</template>


<style scoped>
.outer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2em;
}

.grid-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}
.answer-section {
  width: 100%;
}

.answer-box {
  display: inline-block;
  border-radius: 15px;
  border: 1px solid var(--black);
  text-align: center;
  align-content: center;
  align-items: center;
  color: var(--black);
  max-width: 300px;
  min-width: 20px;

  font-size: 2em;
  padding: 10px;
}

p {
  margin: 20px 0 0;
}

.arrow {
  display: block;
  width: 100px;
  object-fit: contain;
  margin-bottom: 25px;
  filter: var(--filter);
}

.arrow-0 {
  transform: rotate(-45deg);
}

/* .arrow-1 Pas de tranform */

.arrow-2 {
  transform: rotate(45deg);
}

.arrow-3 {
  transform: rotate(-90deg);
}

.arrow-4 {
  transform: rotate(90deg);
}

.arrow-5 {
  transform: rotate(-135deg);
}

.arrow-6 {
  transform: rotate(180deg);
}

.arrow-7 {
  transform: rotate(135deg);
}

* {
  font-family: "Sofia Sans", sans-serif;
  color: var(--text-color);
}
</style>
