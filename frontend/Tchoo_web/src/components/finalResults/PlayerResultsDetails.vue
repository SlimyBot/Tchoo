<script setup>

defineProps({
  playerName: {
    type: String,
    required: true
  },
  score: {
    type: String,
    required: true
  },
  ranking: {
    type: String,
    required: true
  }
})

</script>

<template>
  <div class="wrapper">
    {{ playerName }} - {{ score }} pts {{ ranking }}
  </div>
</template>

<style scoped>

* {
    font-family: 'Sofia Sans', sans-serif;
    color: #17273A;
}

.wrapper {
    height: 10%;
    width: 30%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    @media screen and (max-width: 600px) {
        font-size: 20px;
        width: 75%;
        padding: 10px;
  }
}
    
</style>