<script setup>
import Controls from "../../question/Controls.vue";
import OpenQuestion from "./OpenQuestion.vue";
import QuestionMultiplesAnswers from "./QuestionMultiplesAnswers.vue";

const props = defineProps({
  /* eslint-disable */
  question: {
    type: Object,
    required: true,
  },
  questionType: {
    type: String,
    required: true
  },
  answers: {
    type: Array,
    required: true,
  },
  /* eslint-enable */
});

const emit = defineEmits(["showResults", "pauseAnswers", "nextQuestion", "stopSession"])

function showResults(state) {
  emit("showResults", state)
}

function pauseAnswers(state) {
  emit("pauseAnswers", state)
}

function nextQuestion() {
  emit("nextQuestion")
}

function stopSession() {
  emit("stopSession")
}
</script>

<template>
  <div class="main-container">
    <div class="controls-container">
      <Controls
        @show-results="showResults"
        @pause-answers="pauseAnswers"
        @next-question="nextQuestion()"
        @stop-session="stopSession()"
      />
    </div>

    <OpenQuestion 
      v-if="questionType.includes('open')"
      :question="props.question"
      :is-restricted="questionType === 'open_restricted'"
    />

    <QuestionMultiplesAnswers v-else
                              :question="props.question"
                              :answers="props.answers"
    />
  </div>
</template>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  gap: 1.5em;
}
</style>
