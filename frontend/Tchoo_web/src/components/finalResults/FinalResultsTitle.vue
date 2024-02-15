<script setup>
const changeLanguage = (lang) => {
  this.$i18n.locale = lang;
  this.closeMenu();
};
</script>

<template>
  <div class="div">
    {{ $t("final.result") }}
  </div>
</template>

<style scoped>
* {
  font-family: 'Sofia Sans', sans-serif;
  color: #17273A;
}

.div {
  display: flex;
  justify-content: space-evenly;
  font-size: 30px;

  @media screen and (max-width: 600px) {
    font-size: 20px;
    flex-direction: column;
    align-items: center;
  }
}
</style>