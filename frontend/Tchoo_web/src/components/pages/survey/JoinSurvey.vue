<script setup>
import QrcodeVue from 'qrcode.vue'

defineProps({
  nameSurvey: {
    type: String,
    required: true
  }
})

const url = window.location.href
</script>

<template>
  <div class="wrapper">
    <span>
      {{ nameSurvey }}
    </span>

    <qrcode-vue :value="url"
                :size="300"
    />
  </div>
</template>

<style scoped>

.wrapper {
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 4em;
  font-weight: bold;
  margin-top: 10vh;
  gap: 2vh;
}

span:before {
  content: "";
  display: block;
  width: 33%;
  height: 2px;
  background: var(--main-color);
  left: 0;
  top: 56%;
  position: absolute;
}

span:after {
  content: "";
  display: block;
  width: 33%;
  height: 2px;
  background: var(--main-color);
  right: 0;
  top: 56%;
  position: absolute;
}

@media screen and (min-width: 1000px) {
}

@media screen and (max-width: 1000px) {
}
</style>