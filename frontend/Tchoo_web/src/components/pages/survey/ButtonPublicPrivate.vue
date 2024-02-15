<script setup>
import { ref } from "vue";
const showRegister = ref(false);
</script>

<template>
  <div class="wrapper">
    <input
      id="public"
      type="radio"
      name="typeGame"
      checked
      @click="showRegister = false"
    >
    <input
      id="private"
      type="radio"
      name="typeGame"
      @click="showRegister = true"
    >
    <label
      for="public"
      class="public"
    >
      <span>
        {{ $t("btnPriv.public") }}
        <!-- Public -->
      </span>
    </label>
    <label
      for="private"
      class="private"
    >
      <span>
        {{ $t("btnPriv.private") }}
        <!-- Privée -->
      </span>
    </label>
  </div>
  <div
    v-show="showRegister"
    id="select"
    class="selectDropdown"
  >
    <select>
      <option value="none">
        {{ $t("btnPriv.select") }}
        <!-- Select group -->
      </option>
    </select>
  </div>
</template>

<style scoped>

* {
    font-family: 'Sofia Sans', sans-serif;
    color: var(--text-color);
}
@media screen and (min-width: 1000px) {
  .wrapper {
    display: inline-flex;
    height: 7%;
    width: 30%;
    align-items: center;
    position: absolute;
    top: 85%;
    left: 28%;
    transform: translate(-50%, -50%);
    padding: 15px 10px;
  }
  .wrapper .public {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    border-radius: 10px;
    border: 3px solid lightgrey;
    border-right-style: none;
    transition: all 0.3s ease;
  }
  .wrapper .private {
    width: 100%;
    display: flex;
    margin: 0 -2px;
    align-items: center;
    justify-content: space-evenly;
    border-radius: 10px;
    border: 3px solid lightgrey;
    border-left-style: none;
    transition: all 0.3s ease;
  }
  input[type="radio"] {
    display: none;
  }
  #public:checked:checked ~ .public,
  #private:checked:checked ~ .private {
    border-color: var(--CTA-color);
    background: var(--CTA-color);
  }
  #public:checked:checked ~ .public .dot,
  #private:checked:checked ~ .private .dot {
    background: var(--white);
  }
  .wrapper span {
    font-size: 20px;
    color: #808080;
  }
  #public:checked:checked ~ .public span,
  #private:checked:checked ~ .private span {
    color: var(--white);
  }

  .selectDropdown {
    position: absolute;
    box-sizing: border-box;
    align-items: center;
    top: 85%;
    left: 50%;
    transform: translate(-50%, -50%);
    justify-content: space-evenly;
  }
  .selectDropdown {
    position: absolute;
    border-radius: 10px;
  }
  .selectDropdown select {
    font-size: 20px;
    padding: 8px 24px 8px 10px;
    border: 3px solid lightgrey;
    color: #808080;
    border-radius: 10px;
  }
  .selectDropdown select:active,
  .selectDropdown select:focus {
    outline: none;
  }
}

@media screen and (max-width: 1000px) {
  .wrapper {
    display: inline-flex;
    height: 8%;
    width: 80%;
    align-items: center;
    position: absolute;
    top: 70%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 15px 10px;
  }
  .wrapper .public {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    border-radius: 10px;
    border: 3px solid lightgrey;
    border-right-style: none;
    transition: all 0.3s ease;
  }
  .wrapper .private {
    height: 100%;
    width: 100%;
    display: flex;
    margin: 0 -2px;
    align-items: center;
    justify-content: space-evenly;
    border-radius: 10px;
    border: 3px solid lightgrey;
    border-left-style: none;
    transition: all 0.3s ease;
  }
  input[type="radio"] {
    display: none;
  }
  #public:checked:checked ~ .public,
  #private:checked:checked ~ .private {
    border-color: var(--CTA-color);
    background: var(--CTA-color);
  }
  #public:checked:checked ~ .public .dot,
  #private:checked:checked ~ .private .dot {
    background: var(--white);
  }
  .wrapper span {
    font-size: 20px;
    color: #808080;
  }
  #public:checked:checked ~ .public span,
  #private:checked:checked ~ .private span {
    color: var(--white);
  }

  .selectDropdown,
  .selectDropdown * {
    position: absolute;
    box-sizing: border-box;
    align-items: center;
    justify-content: space-evenly;
    top: 80%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .selectDropdown {
    position: absolute;
    border-radius: 10px;
  }
  .selectDropdown select {
    font-size: 20px;
    padding: 8px 24px 8px 10px;
    border: 3px solid lightgrey;
    color: #808080;
    border-radius: 10px;
  }
  .selectDropdown select:active,
  .selectDropdown select:focus {
    outline: none;
  }
}
</style>
