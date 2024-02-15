<script setup>

import ClearButton from "@/components/ClearButton.vue";
import GearHeader from "@/components/Gear.vue";
</script>

<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >


  <body>
    <h1>403</h1>
    <p class="msg">
      {{ $t("error403.msg")  }}
      <!-- This page is not accessible -->
    </p>
    <!-- TODO Translation -->
    <div class="trespassing">
      <span class="material-symbols-outlined">
        block
      </span>
    </div>
    <div class="return">
      <ClearButton to="/">
        {{ $t("error403.home") }}
      </ClearButton>
    </div>
    <GearHeader />
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

 .material-symbols-outlined {
   font-variation-settings:
       'FILL' 0,
       'wght' 400,
       'GRAD' 0,
       'opsz' 48;
   font-size: 80px !important;
 }

  .trespassing {
    text-align: center;
    color: var(--text-color);
  }

  .msg {
    font-size: 50px;
    text-align: center;
    margin-top: -50px;
    color: var(--text-color);

    font-family: "Sofia Sans", sans-serif;
  }

  .return {
    margin-left: auto;
    margin-right: auto;
    margin-top: 250px;
  }

</style>