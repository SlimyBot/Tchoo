<script setup>
defineProps({
  time: {
    type: String,
    required: false,
    default: "∞",
  },
  nb: {
    type: String,
    required: false,
    default: "8",
  }
});
</script>

<template>
  <div>
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
    >

    <div class="timer">
      <p class="time">
        <span
          class="material-symbols-outlined"
        >
          timer
        </span>
        {{ time }}'
      </p>
      <div class="nb">
        <p>
          {{ nb }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
      'FILL' 0,
      'wght' 300,
      'GRAD' 0,
      'opsz' 24;
  color: var(--white);
}

.timer {
  display: block;
  position: absolute;
  margin-left: 70%;
  border: #D9D9D9 2px solid;
  border-radius: 100%;
  width: 150px;
  height: 150px;

  align-items: center;
  justify-content: center;
}

.nb {
  display: flex;
  align-items: center;
  justify-content: center;

  border: var(--CTA-color) 2px solid;
  border-radius: 100%;
  width: 100px;
  height: 100px;

  margin: auto;
  margin-top: -13px;
}

.nb p {
  font-size: 50px;
  font-family: 'Sofia Sans', sans-serif;
  color: var(--text-color);
}

.time {
  background-color: white;
  text-align: center;
  color: #D9D9D9;
  font-size: 20px;
  margin-top: -10px;

  width: fit-content;
  padding-left: 10px;
  padding-right: 10px;
  margin-left: auto;
  margin-right: auto;
}

span {
  color: #D9D9D9
}
</style>