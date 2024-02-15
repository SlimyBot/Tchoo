<script setup>
import { useRouter } from 'vue-router';

import { BASE_URL } from "@/lib/baseURL.js";
import { logout } from '@/lib/auth';

const router = useRouter();

async function disconnect() {
  logout();

  const res = await window.fetch(`${BASE_URL}/cas/logout_url`)
  const url = (await res.json()).url

  window.location.href = url
}
</script>

<template>
  <div class="divHeader">
    <div class="left">
      <img src="../assets/UCAlogoQhaut.png"
           alt="LOGO UCA"
           class="logo"
      >
      <h3 class="headerTcho">
        <router-link to="/">
          UniCA <i> Tchoo </i>
        </router-link>
      </h3>


      <router-link
        to="/join"
        class="btnJoin"
      >
        {{ $t("head.joinSession") }}
      </router-link>
    </div>

    <div class="right">
      <button
        class="leave"
        @click="disconnect()"
      >
        <img src="@/components/icons/leave.svg"
             alt="Exit"
        >
      </button>
    </div>
  </div>
</template>

<style scoped>
* {
  font-family: "Rubik Mono One", sans-serif;
  color: var(--main-color);
}

/*
********************************************************************************************************
********************************************************************************************************
css de l'header
********************************************************************************************************
********************************************************************************************************
*/

.logo {
  width: 50px;
  height: 50px;
  margin-left: 10px;
}

h3 {
  display: inline-block;
  font-size: 2em;
  margin-right: 70px;
  margin-left: 10px;
}

h3 i {
  font-size: 0.5em;
  font-family: "Rubik Mono One", sans-serif;
  color: var(--main-color);
  margin-left: -1em;
}

.divHeader {
  display: flex;
  flex-direction:row;
  justify-content: space-between;
  align-items: center;
  width: 98%;
  /* margin-bottom: 500px; */
}

.left{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.btnJoin{
  display: inline-block;
  border: solid 1px var(--main-color);
  background-color: var(--white);
  border-radius: 30px;
  padding: 10px 30px;
  color: var(--text-color);
  cursor: pointer;
  font-size: 0.8em;
  transition: 800ms;
  text-decoration: none;

  font-family: "Sofia Sans", sans-serif;
}

.btnJoin:hover{
  background-color: var(--CTA-color);
  color: white;
  transition: 800ms;
}

.right{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.leave{
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.leave img{
  width: 40px;
  height: 40px;
  transition: 700ms;
  filter: var(--filter);
}

.leave img:hover{
  width: 50px;
  height: 50px;
  transition: 700ms;
}


/*
********************************************************************************************************
********************************************************************************************************
css responsive
********************************************************************************************************
********************************************************************************************************
*/

@media screen and (max-width: 700px) {
  .divHeader {
    width: 90%;
  }

  .headerTcho{
    margin-right: 20px;
  }
}

@media screen and (max-width: 600px) {

  .left{
    margin-top: -10px;
    margin-left: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .right {
    margin-top: -10px;
    margin-left: -50px;
    display: flex;
    flex-direction: column-reverse;
    justify-content: center;
    align-items: center;
  }

  .logo {
    display: none;
  }

  h3 {
    font-size: 1.5em;
    margin-right: 0;
    margin-left: 0;
  }

  .btnJoin{
    display: inline-block;
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: 0.6em;
  }

  .divHeader {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 98%;
  }
}
</style>

<style>
h3 a {
  text-decoration: none;
}
</style>
