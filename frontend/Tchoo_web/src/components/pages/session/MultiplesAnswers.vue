<script setup>
import Timer from "@/components/question/Timer.vue";
import Gear from "@/components/Gear.vue";
import ArrowButton from "@/components/ArrowButton.vue";

import { ref } from "vue"
import Header from "@/components/Header.vue";

const props = defineProps({ nbAnswers: { type: Number, required: true } })

const emit = defineEmits(["answer"])

const clickedArrows = ref({
  top_left: false,
  top: false,
  top_right: false,
  left: false,
  right: false,
  bottom_left: false,
  bottom: false,
  bottom_right: false
})

function middleButtonClick() {
  emit("answer", clickedArrows.value);
}

function activeIf(number) {
  return number <= props.nbAnswers
}
</script>

<template>
  <Header />
  <main>
    <div class="arrow-grid">
      <div class="top_left"
           style="margin-bottom:-2.5em; margin-right: -2.5em "
      >
        <div class="button">
          <ArrowButton
            :rotation="-45"
            :active="activeIf(1)"
            @clicked="(state) => clickedArrows.top_left = state"
          />
        </div>
      </div>
      <div class="top">
        <div class="button">
          <ArrowButton
            :padding="70"
            :active="activeIf(2)"
            @clicked="(state) => clickedArrows.top = state"
          />
        </div>
      </div>
      <div class="top_right"
           style="margin-left:-2.5em; margin-bottom: -2.5em "
      >
        <div class="button">
          <ArrowButton
            :rotation="45"
            :active="activeIf(3)"
            @clicked="(state) => clickedArrows.top_right = state"
          />
        </div>
      </div>
      <div class="left">
        <div class="button">
          <ArrowButton
            :rotation="-90"
            :padding="70"
            :active="activeIf(4)"
            @clicked="(state) => clickedArrows.left = state"
          />
        </div>
      </div>
      <div class="middle">
        <label class="">
          <button
            class="MiddleButton"
            @click="middleButtonClick()"
          >
            {{ $t("multipleAnsw.answer") }}
            <!-- Répondre -->
          </button>
        </label>
      </div>
      <div class="right">
        <div class="button">
          <ArrowButton
            :rotation="90"
            :active="activeIf(5)"
            @clicked="(state) => clickedArrows.right = state"
          />
        </div>
      </div>
      <div class="bottom_left"
           style="margin-top:-2.5em; margin-right: -2.5em "
      >
        <div class="button">
          <ArrowButton
            :rotation="-135"
            :active="activeIf(6)"
            @clicked="(state) => clickedArrows.bottom_left = state"
          />
        </div>
      </div>
      <div class="bottom">
        <div class="button">
          <ArrowButton
            :rotation="180"
            :active="activeIf(7)"
            @clicked="(state) => clickedArrows.bottom = state"
          />
        </div>
      </div>
      <div class="bottom_right"
           style="margin-top:-2.5em; margin-left: -2.5em "
      >
        <div class="button">
          <ArrowButton
            :rotation="135"
            :active="activeIf(8)"
            @clicked="(state) => clickedArrows.bottom_right = state"
          />
        </div>
      </div>
    </div>
    <!-- <Timer  nb="1"  time="30"/> Timer désactivé pour l'instant -->
  </main>
  <Gear />
</template>

<style scoped>

* {
  font-family: "Sofia Sans", sans-serif;
  color: var(--text-color);
  font-size: large;
}

/*
********************************************************************************************************
********************************************************************************************************
css responsive
********************************************************************************************************
********************************************************************************************************
*/

.arrow-grid {
  display: grid;
  grid-template-columns: repeat(3, auto);
  grid-template-rows: repeat(3, auto);
  align-items: center;
  justify-items: center;
}

.button {
  background-color: transparent;
  max-width: 170px;
  max-height: 170px;
  min-width: 130px;
  min-height: 130px;
  width: 10vw;
  height: 10vw;
  margin: -20px;
}

.MiddleButton {
  background-color: transparent;
  border: var(--main-color) solid 1px;
  width: 20vw;
  height: 20vw;
  min-width: 200px;
  min-height: 200px;
  max-width: 320px;
  max-height: 320px;
  border-radius: 50%;

}

button:hover {
  background-color: var(--main-color);
  cursor: pointer;
  color: var(--white);
}

main {
  width: 97vw;
  height: 90vh;
  background-image: url("../../icons/BG_Multiples_Answers.png");
  background-size: cover;
  background-position: center;

  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  margin: auto;
}
</style>