<script setup>
defineProps({
  number: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <div class="wrapper">
    {{ $t('numberPlayers.nbrPly')  }}
    <!-- Nombre de joueurs -->
    <span> {{ number }} </span>
  </div>
</template>

<style scoped>

.wrapper {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  text-align: center;
  font-size: 20px;
  margin-top: 20px;
}

</style>