<script setup>
import ClearButton from "@/components/ClearButton.vue";
import Gear from "@/components/Gear.vue";


</script>

<template>
  <body>
    <h1> 404 </h1>
    <p class="notFound">
      {{ $t("error404.notFound") }}
    </p>
    <div class="return">
      <ClearButton to="/">
        {{ $t("error404.home") }}
      </ClearButton>
    </div>
    <Gear /> 
  </body>
</template>

<style scoped>

h1 {
  font-size: 100px;
  text-align: center;
  margin-top: 200px;
  color: var(--text-color);

  font-family: "Rubik Mono One", sans-serif;
}

.notFound {
  font-size: 50px;
  text-align: center;
  margin-top: -50px;
  color: var(--text-color);

  font-family: "Rubik Mono One", sans-serif;
}

.return {
  margin-left: auto;
  margin-right: auto;
  margin-top: 250px;
}


</style>