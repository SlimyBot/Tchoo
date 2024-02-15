<script setup>
import ButtonStartTest from "@/components/pages/survey/ButtonStartTest.vue";
import JoinSurvey from "@/components/pages/survey/JoinSurvey.vue";
import NumberPlayers from "@/components/pages/survey/NumberPlayers.vue";
import SurveyTimeTotal from "@/components/pages/survey/SurveyTimeTotal.vue";
import Header from "@/components/Header.vue";
import Gear from "@/components/Gear.vue";

const props = defineProps({
  /* eslint-disable */
    surveyName: String,
    playerCount: Number,
    surveyTime: String
  /* eslint-enable */
})

defineEmits(["startSurvey"])
</script>

<template>
  <Header />
  <JoinSurvey :name-survey="props.surveyName" />
  <NumberPlayers :number="props.playerCount" />
  <ButtonStartTest @start-test="$emit('startSurvey')" />
  <Gear />
</template>

<style scoped>
* {
    font-family: 'Sofia Sans', sans-serif;
    color: var(--text-color);
}
</style>
