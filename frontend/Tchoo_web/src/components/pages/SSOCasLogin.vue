<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { BASE_URL } from "@/lib/baseURL.js";
import { saveToken, isTeacher } from "@/lib/auth.js";

const loginState = ref("loading")

const router = useRouter()
const route = useRoute()

const ticket = route.params.ticket

onMounted(async () => {
  if (!ticket) {
    const res = await window.fetch(`${BASE_URL}/cas/login`)

    window.location.href = (await res.json()).url
    return
  }

  router.replace("/casLogin")
  // Validation du ticket
  const res = await window.fetch(`${BASE_URL}/cas/login?ticket=${ticket}`, {
    method: "POST"
  })

  const json = await res.json()

  if (json.stage === "failed_login") {
    loginState.value = "failed"
    return
  }

  loginState.value = "success"
  saveToken(json.token.access_token)

  if (isTeacher()) {
    router.push("/surveys");
  } else {
    router.push("/results")
  }

})
</script>

<template>
  <router-link to="/">
    {{ $t ("cas.home") }}
    <!-- Retour à l'accueil -->
  </router-link>


  <h1>
    {{ $t ("cas.login")  }}
    <!-- Login en cours -->
  </h1>

  <div v-if="loginState === 'loading'"
       class="state"
  >
    {{ $t ("cas.loading") }}
    <!-- Chargement... -->
  </div>

  <div v-else-if="loginState === 'failed'"
       class="state"
  >
    {{ $t ("cas.error") }}
    <!-- Erreur de connexion. Veillez réessayer. -->
  </div>

  <div v-else
       class="state"
  >
    {{ $t ("cas.welcome") }}
    <!-- Bienvenue ! -->
  </div>

  <div class="divLoad">
    <span class="loader"/>
  </div>
</template>

<style scoped>

* {
  font-family: "Sofia Sans", sans-serif;
  color: var(--text-color);
}

.state{
  text-align: center;
  color: rgb(215, 215, 215);
}

h1 {
  font-family: "Rubik Mono One", sans-serif;
  text-align: center;
  margin-top: 200px;
  font-weight: 100;
  margin-bottom: 5px;
}

.loader, .loader:before, .loader:after {
  border-radius: 50%;
  width: 2.5em;
  height: 2.5em;
  animation-fill-mode: both;
  animation: bblFadInOut 1.8s infinite ease-in-out;
}
.loader {
  color: var(--text-color);
  position: relative;
  text-indent: -9999em;
  transform: translateZ(0);
  animation-delay: -0.16s;
}
.loader:before,.loader:after {
  content: '';
  position: absolute;
  top: 0;
}
.loader:before {
  left: -3.5em;
  animation-delay: -0.32s;
}
.loader:after {
  left: 3.5em;
}

@keyframes bblFadInOut {
  0%, 80%, 100% { box-shadow: 0 2.5em 0 -1.3em }
  30% { box-shadow: 0 2.5em 0 0 }
}

.divLoad{
  padding-left: 7vh;
  margin-top: 30px;
  align-items: center;
  text-align: center;
  width: 90vw;
  height: 20vh;
}
    


</style>