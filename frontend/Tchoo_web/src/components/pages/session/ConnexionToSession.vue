<script setup>
import Gear from "@/components/Gear.vue";
const components = {
  Gear
};

defineProps({
  code: {
    type: String,
    required: false,
    default: "CSMBANGER",
  },
});
</script>

<template>
  <div class="msg">
    <h1>{{ $t ("lobby.conn") }}</h1>
    <p>{{ $t("lobby.Code") }} : {{ code }} </p>
    <span class="loader" />
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