<script setup>
import {ref, onMounted} from "vue";
import {useRoute} from "vue-router";
import {get_all_players_end_survey,} from "@/lib/requests.js"

const all_players = ref({})
const route = useRoute();
const sessionId = route.params.session_id;

onMounted(async () => {
  let statusCode;
  let json;
  [json, statusCode] = get_all_players_end_survey(6);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  console.log(json)


  all_players.value = json;
  console.log(all_players);
})

</script>

<template>
  <h1>
    {{ $t("allPlayers.result")  }}
    <!-- Résultats complets -->
  </h1>
</template>

<style scoped>

</style>