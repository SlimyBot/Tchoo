<script setup>
import Gear from "@/components/Gear.vue";
const components = {
  Gear
};

defineProps({
  errorMsg: {
    type: String,
    required: false,
    default: "404",
  },
});
</script>

<template>
  <div class="msg">
    <h1>{{ $t ("error.error") }} : {{ errorMsg }}</h1>
    <p>{{ $t("error.msg") }}</p>
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
</style>