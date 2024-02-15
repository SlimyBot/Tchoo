<script setup>

defineProps({
  playerName: {
    type: String,
    required: true
  },
  score: {
    type: Number,
    required: true
  },
  ranking: {
    type: Number,
    required: true
  }
})

</script>

<template>
  <div class="wrapper">
    {{ playerName }} - {{ score }} pts
    <div class="ranking">
      {{ ranking }}
    </div>
  </div>
</template>

<style scoped>

* {
    font-family: 'Sofia Sans', sans-serif;
    color: #17273A;
}

.wrapper {
    margin-top: 2%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 20px;
    border-radius: 10px;
    border: 2px solid rgb(236, 236, 236);
    padding: 10px 10px;
    padding-left: 5%;
    padding-right: 2%;

    transition: 0.15s ease-in-out;
    @media screen and (max-width: 1000px) {
        width: 75%;
  }
}

.ranking {
    margin-left: 5%;
    font-weight: 600;
    margin-right: 5%;
}

a {
    text-decoration: none;
    color: inherit;
    display: block;
}

.wrapper:hover{
    background-color: rgb(245, 245, 245);
    box-shadow: 7px 7px 15px -10px rgba(79, 112, 164, 0.15);
    border-color: rgb(245, 245, 245);;

    transition: 0.4s ease-in-out;
}

</style>