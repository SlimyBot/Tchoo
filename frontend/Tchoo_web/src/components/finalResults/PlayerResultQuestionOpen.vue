<script setup>

defineProps({
  questionNumber: {
    type: String,
    required: true
  },
  question: {
    type: String,
    required: true
  },
  answer: {
    type: String,
    required: true
  }
})

</script>

<template>
  <div class="wrapper">
    <div class="number">
      {{ questionNumber }}
    </div>
    <div class="content">
      <div class="question">
        {{ question }}
      </div>
      <div class="answer">
        <ul>
          <li v-for="(char, index) in answer"
              :key="index"
          >
            {{ char }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

* {
    font-family: 'Sofia Sans', sans-serif;
    color: #17273A;
}

.wrapper {
    margin-top: 2%;
    height: 10%;
    width: 60%;
    display: flex;
    align-items: center;
    text-align: center;
    font-size: 20px;
    background: rgba(106, 94, 94, 0.3);
    border-radius: 10px;
    @media screen and (max-width: 600px) {
        flex-direction: column;
        height: auto;
        width: 90%;
  }
}

.content {
    margin: auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-right: 5%;
}

.question {
    margin-bottom: 10px;
    margin-top: 10px;
}

.number {
    padding: 3%;
}

.type {
    padding: 3%;
}

</style>