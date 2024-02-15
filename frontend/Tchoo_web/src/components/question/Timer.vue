<script setup>
defineProps({
  timeLeft: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="timerStyle" />
  <div class="timer">
    {{ timeLeft }}
  </div>
</template>

<style scoped>
* {
  font-family: "Rubik Mono One", sans-serif;
  color: #070819;
}
.timer {
  height: 75px;
  width: 75px;
  border: 1px solid #130f0f;
  border-radius: 50%;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  left: 75%;
  transform: translate(-50%, -50%);
  right: auto;
}

.timerStyle {
  height: 90px;
  width: 90px;
  border: 1px solid #130f0f;
  border-radius: 60%;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  left: 75%;
  transform: translate(-50%, -50%);
  right: auto;
}
</style>
