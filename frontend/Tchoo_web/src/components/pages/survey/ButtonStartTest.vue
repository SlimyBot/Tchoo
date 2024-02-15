<script setup>
defineEmits(["startTest"])
</script>

<template>
  <div class="wrapper">
    <button
      class="start"
      @click="$emit('startTest')"
    >
      {{ $t("btnStart.start") }}
      <!-- Lancer le test -->
    </button>
  </div>
</template>

<style scoped>
* {
    font-family: 'Sofia Sans', sans-serif;
    color: var(--text-color);
    cursor: pointer;
}

.wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 20px;
    margin-top: 20vh;

}

@media screen and (min-width: 1000px) {
    .start {
        font-size: 20px;
        color: var(--CTA-color);
        background: var(--white);
        border-radius: 30px;
        border: 3px solid var(--CTA-color);
        text-align: center;
        width: 50%;
        padding: 20px 40px;
    }
    .start:hover{
        background-color: var(--CTA-color);
        color: var(--white);
        border: none;
    }
}

@media screen and (max-width: 1000px) {
    .start {
        font-size: 1em;
        padding: 20px 40px;
        color: var(--main-color);
        background: var(--white);
        border-radius: 30px;
        border: 3px solid var(--CTA-color);
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: space-evenly;
    }
    .start:hover{
        background-color: var(--CTA-color);
        color: var(--white);
        border: none;
    }
}
</style>