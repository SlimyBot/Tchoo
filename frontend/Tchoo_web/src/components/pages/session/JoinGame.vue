<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Gear from '@/components/Gear.vue';
import Header from "@/components/Header.vue";

const router = useRouter()
const joinCode = ref("")

function joinClick() {
  if (joinCode.value.length === 0) return;

  router.push("/session/" + joinCode.value)
}
</script>

<template>
  <body>
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
    >
    <Header />
    <main>
      <Gear />
      <div class="return">
        <button class="btnReturn">
          <img
            src="@/components/icons/return.svg"
            alt="return"
            @click="router.push('/surveys')"
          >
        </button>
      </div>
      <div>
        <h1>{{$t('joinGame.code')}}</h1>
      </div>
      <div>
        <div class="wrapper">
          <label>
            <p style="display: none">Code</p>
            <input
              id="name"
              v-model="joinCode"
              name="name"
              type="text"
              :placeholder="$t('joinGame.code')"
              required
            >
          </label>
          <label>
            <p style="display: none">Submit</p>
            <button
              class="connect"
              @click="joinClick()"
            >
              <span class="material-symbols-outlined">
                arrow_forward
              </span>
            </button>
          </label>
        </div>
      </div>
    </main>
    <div class="style"/>
  </body>
</template>

<style scoped>
main {
    align-items: center;
    justify-content: center;

    overflow: hidden;
    font-family: "Sofia Sans", sans-serif;
    margin-top: 50px;
}

h1 {

    display: block;
   margin-left: 50px;
    font-size: 30px;
    color: var(--main-color);
    margin-bottom: 50px;
}

h1:after {
    content: '';
    display: inline-block;
    width: 70%;
    height: 2px;
    background: var(--main-color);
    position: relative;
    top: -0.2em;
    margin-left: 10px;
}

body {
  margin: -8px;
  padding: 0;
  height: 100vh;
  background: var(--background);
}

.wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;

  margin-top: 10vh;

}

.connect {
    font-size: 30px;
    color: var(--white);
    background: var(--main-color);
    border-radius: 100px;
    border: 3px solid var(--white);
    text-align: center;
    width: 80px;
    height: 60px;
    display: inline-block;
    margin-left: 40px;
    transition: 0.1s ease-in-out;
}

.connect:hover {
    cursor: pointer;
    background: var(--white);
    border: 3px solid var(--CTA-color);
    color: var(--main-color);
    transition: 0.1s ease-in-out;
}

input {
    height: 50px;
    width: 40vw;
    border-radius: 30px;
    border: 1px solid var(--black);
    font-size: 20px;
    text-align: center;
}

::placeholder {
    text-align: center;
}

.material-symbols-outlined {
   font-variation-settings:
       'FILL' 0,
       'wght' 200,
       'GRAD' 0,
       'opsz' 24
}

.btnReturn {
  background-color: transparent;
  border: none;
  border-radius: 100%;
  cursor: pointer;
  transition: 500ms;
  margin-left: 5vw;
  margin-top: 5vh;
  filter: var(--filter);
}

.btnReturn:hover {
  border-radius: 30px;
  transition: 500ms;
}

</style>