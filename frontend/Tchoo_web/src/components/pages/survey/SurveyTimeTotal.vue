<script setup>
defineProps({
  time: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <div class="wrapper">
    <span class="material-symbols-outlined"> timer </span>
    {{ time }}
  </div>
</template>

<style scoped>
* {
    font-family: 'Sofia Sans', sans-serif;
    color: var(--text-color);
}

@media screen and (min-width: 1000px) {
  .wrapper {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    position: absolute;
    top: 60%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    font-size: 20px;
  }
}

@media screen and (max-width: 1000px) {
  .wrapper {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    position: absolute;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    font-size: 20px;
  }
}
</style>
