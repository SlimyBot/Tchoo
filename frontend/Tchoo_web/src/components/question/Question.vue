<script setup>
defineProps({
  question: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <div class="box">
    {{ question }}
  </div>
</template>

<style scoped>
.box {
  font-family: "Sofia Sans", sans-serif;
  font-size: 2.5em;
  color: var(--text-color);

  width: 700px;
  max-width: 90%;
  height: 200px;

  border-radius: 10px;
  border: 1px solid var(--main-color);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1em;
}
</style>
