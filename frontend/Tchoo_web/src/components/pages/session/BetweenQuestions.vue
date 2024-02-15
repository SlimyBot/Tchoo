<script setup>

import Gear from "@/components/Gear.vue";
const components = {
  Gear
};

</script>

<template>
  <div class="msg">
    <h1>{{ $t ("between.Answer") }}</h1>
    <span class="loader" />
    <p class="wait">
      {{ $t("between.msg") }}
    </p>
    <Gear />
  </div>
</template>

<style scoped>
.msg {
  text-align: center;
  margin-top: 40vh;
}

.msg h1 {
  font-family: "Rubik Mono One", sans-serif;
  color: var(--text-color);
}

.msg p {
  font-family: "Sofia Sans Light", sans-serif;
  color: var(--text-color);
  font-size: 1.5em;

  margin-top: -20px;
}

.msg .wait {
  font-family: "Sofia Sans Light", sans-serif;
  color: var(--text-color);
  font-size: 1.5em;

  margin-top: 20px;
}

.loader {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: inline-block;
  border-top: 3px solid var(--main-color);
  border-right: 3px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>