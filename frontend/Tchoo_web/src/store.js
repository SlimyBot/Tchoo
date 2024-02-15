import { createStore } from "vuex";

export default createStore({
  state: {
    appLanguage: localStorage.getItem("appLanguage") || import.meta.env.VUE_APP_I18N_LOCALE || 'fr'
  },
  getters: {
    getAppLanguage: (state) => state.appLanguage
  },
  mutations: {
    setAppLanguage(state, language) {
      state.appLanguage = language;
      localStorage.setItem("appLanguage", language);
    }
  }
});