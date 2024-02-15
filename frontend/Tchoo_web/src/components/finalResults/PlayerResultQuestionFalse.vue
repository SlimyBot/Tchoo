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
    type: Array,
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
          <li v-for="(answerIndex) in answer"
              :key="answerIndex"
          >
            {{ answerIndex }}
          </li>
        </ul>
      </div>
    </div>
    <div class="type">
      &#10060;
    </div>
  </div>
</template>

<style scoped>

* {
    font-family: 'Sofia Sans', sans-serif;
    color: #17273A;
}

.wrapper {
    height: 10%;
    width: 60%;
    display: flex;
    justify-content: space-between; 
    align-items: center;
    font-size: 20px;
    background: rgba(175, 76, 79, 0.3);
    border-radius: 10px;
    @media screen and (max-width: 600px) {
        flex-direction: column;
        height: auto;
        width: 90%;;
  }
}

.content {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
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