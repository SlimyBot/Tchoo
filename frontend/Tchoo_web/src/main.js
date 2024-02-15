import "./assets/main.css";

// main.js

import { createApp } from "vue";
import App from "./App.vue";
import router from "./lib/router";
import { createI18n } from "vue-i18n";
import store from "./store";

// Importez les fichiers de traduction pour chaque langue
import frMessages from "./locales/fr.json";
import ruMessages from "./locales/ru.json";
import enMessages from "./locales/en.json";
import itMessages from "./locales/it.json";
import esMessages from "./locales/es.json";
import jpMessages from "./locales/jp.json";

// Initialisez localStorage avec la valeur du store
const savedLanguage = localStorage.getItem("appLanguage") || "fr";

// Utilisez la langue sauvegardée comme langue par défaut dans I18n et dans le store Vuex
const i18n = createI18n({
  locale: savedLanguage,
  messages: {
    fr: frMessages,
    ru: ruMessages,
    en: enMessages,
    it: itMessages,
    es: esMessages,
    jp: jpMessages,
    // Ajoutez d'autres langues au besoin
  },
});

// Mettez à jour la langue du store Vuex au démarrage
store.commit("setAppLanguage", savedLanguage);

createApp(App).use(i18n).use(router).use(store).mount("#app");
