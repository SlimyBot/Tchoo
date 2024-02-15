<script setup>
import Gear from "@/components/Gear.vue"
import ClearButton from "../ClearButton.vue";
const components = {
  Gear
};

</script>

<template>
  <div class="Tot">
    <div class="divMain">
      <div class="divMainIndex">
        <h1 class="h1Tchoo">
          <img src="../../assets/UCAlogoQhaut.png"
               alt="UCA LOGO"
               class="logo"
          >
          UniCA <i> Tchoo </i>
        </h1>
        <p class="textIndex">
          {{ $t("main.surveySolution") }}
        </p>
      </div>
      <div>
        <img
          src="@/assets/Frame41.png"
          alt="Echelle"
          class="LadderTop"
        >
      </div>
    </div>
    <div class="footer">
      <div class="login">
        <ClearButton to="/casLogin">
          {{ $t("main.connect") }}
        </ClearButton>
      </div>
      <Gear />
    </div>
  </div>
</template>

<style scoped>
* {
  font-family: "Rubik Mono One", sans-serif;
  color: var(--text-color);
}

/*
********************************************************************************************************
********************************************************************************************************
css du main
********************************************************************************************************
********************************************************************************************************
*/

.Tot {
  height: 80vh;
}

.logo {
  width: 8%;
  height: auto;
  margin: 0 0 0 1%;
}

.divMain {
  display: flex;
  flex-direction: row;
}

.divMainIndex {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h1 {
  font-size: 6em;
  font-family: "Rubik Mono One", sans-serif;
  justify-content: flex-start;
  align-items: flex-start;
  margin: 0;
  margin-top: 17vh;
  vertical-align: middle;

  color: var(--main-color);
}

h1 i {
  font-size: 0.5em;
  font-family: "Rubik Mono One", sans-serif;
  color: var(--main-color);
  margin-left: -1em;
}

.textIndex {
  font-family: "Sofia Sans", sans-serif;
  font-size: 2em;
  justify-content: flex-start;
  align-items: flex-start;
}

.LadderTop {
  width: 30%;
  height: 100%;
  z-index: auto;
}

/*
********************************************************************************************************
********************************************************************************************************
css du footer
********************************************************************************************************
********************************************************************************************************
*/

.footer {
  background: var(--CTA-color);
  color: var(--white);
  text-align: center;
  font-size: 20px;
  height: 37vh;
  bottom: 0;
  right: 0;
  left: 0;
  margin: auto;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-end;
  z-index: auto;
}

.login {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: flex-end;
  margin: 2% 5% 0 0;
  border-radius: 20px;

  background-color: var(--white);
  border: var(--white) 1px solid;
}

.buttonIndex {
  font-family: "Sofia Sans", sans-serif;
  font-size: 1.2em;
  width: 25%;
  height: auto;
  border-radius: 20px;
  margin: 2% 5% 0 0;
  background-color: var(--white);
  border: none;
  padding: 10px;
  transition: 900ms;
}


.href {
  font-family: "Sofia Sans", sans-serif;
  font-size: 1.2em;
  width: max-content;
  height: max-content;
  text-decoration: none;
  transition: 700ms;
}


/*
********************************************************************************************************
********************************************************************************************************
css responsive
********************************************************************************************************
********************************************************************************************************
*/

@media screen and (max-width: 1000px) {
  .divMain {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 5% 10% 0 5%;
  }

  h1 {
    font-size: 3em;
  }

  .textIndex {
    font-size: 1.8em;
  }

  .LadderTop {
    display: none;
  }

  .footer {
    display: flex;
    align-items: center;
    height: 60vh;
  }

  .buttonIndex {
    margin-top: 5%;
    width: 50%;
    height: auto;
  }

}

@media screen and (max-width: 700px) {
  .divMain{
    margin: 5% 10% 0 2%;
  }

  h1 {
    font-size: 3em;
  }

  .footer {
    display: flex;
    align-items: center;
    height: 60vh;
  }

  .buttonIndex {
    margin-top: 5%;
    width: 75%;
    height: auto;
  }
}

@media screen and (max-height: 800px){
  h1 {
    font-size: 4em;
  }

  .divMainIndex{
    margin: 5% 5% 0 2%;
  }
}

@media screen and (max-height: 600px){
  h1 {
    font-size: 3em;
  }

  .divMainIndex{
    margin: 0% 10% 0 2%;
  }
}

@media screen and (max-height: 700px) and (max-width: 1300px){

  h1 {
    font-size: 2em;
  }

  .divMainIndex{
    margin: 0% 10% 0 2%;
  }
}
</style>
