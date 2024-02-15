<script>
export default {
  name: "GearHeader",
  data() {
    return {
      isMenuOpen: false,
      canChangeTheme: import.meta.env.VITE_ALLOW_CHANGE_THEME === "1"
    };
  },
  mounted(){
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
      this.addDarkTheme();
    } else if (currentTheme === 'uca') {
      this.addUCATheme();
    } else if (currentTheme === 'tchoo') {
      this.addTchooTheme();
    }
  },
  methods: {
    async changeLanguage(lang) {
      // Force le chargement de la langue de manière asynchrone
      await import(`@/locales/${lang}.json`).then(messages => {
        this.$i18n.setLocaleMessage(lang, messages.default);
      });

      // Change la langue
      this.$i18n.locale = lang;
      this.closeMenu();

      // Sauvegarde de la langue dans le LocalStorage
      localStorage.setItem("appLanguage", lang);
    },
    isLanguageLoaded(lang) {
      return this.$i18n.te(lang);
    },
    openMenu() {
      this.isMenuOpen = true;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
    addDarkTheme(){
      const htmlTag = document.querySelector('html');
      htmlTag.style.backgroundColor = 'var(--background)';
      htmlTag.classList.remove(...htmlTag.classList);
      htmlTag.classList.add('darkTheme');
      localStorage.setItem("theme","dark");
    },
    addUCATheme(){
      const htmlTag = document.querySelector('html');
      htmlTag.style.backgroundColor = 'var(--background)';
      htmlTag.classList.remove(...htmlTag.classList);
      localStorage.setItem("theme","uca");
    },
    addTchooTheme(){
      const htmlTag = document.querySelector('html');
      htmlTag.style.backgroundColor = 'var(--background)';
      htmlTag.classList.remove(...htmlTag.classList);
      htmlTag.classList.add('tchooTheme');
      localStorage.setItem("theme","tchoo");
    },
  },
};
</script>

<template>
  <div class="divGear">
    <div class="gearDiv"
         @mouseover="openMenu"
         @mouseleave="closeMenu"
    >
      <img src="@/assets/gearG.png"
           alt="Menu"
           class="gear"
      >
      <ul v-if="isMenuOpen"
          class="flagMenu"
      >
        <li :class="{ 'loaded-flag': isLanguageLoaded('fr') }"
            @click="changeLanguage('fr')"
        >
          <img src="@/assets/fr-flag.png"
               alt="French Flag"
               class="flag"
          >
        </li>
        <li :class="{ 'loaded-flag': isLanguageLoaded('en') }"
            @click="changeLanguage('en')"
        >
          <img src="@/assets/en-flag.png"
               alt="English Flag"
               class="flag"
          >
        </li>
        <li :class="{ 'loaded-flag': isLanguageLoaded('ru') }"
            @click="changeLanguage('ru')"
        >
          <img src="@/assets/ru-flag.png"
               alt="Russian Flag"
               class="flag"
          >
        </li>
        <li :class="{ 'loaded-flag': isLanguageLoaded('es') }"
            @click="changeLanguage('es')"
        >
          <img src="@/assets/es-flag.png"
               alt="Spanish Flag"
               class="flag"
          >
        </li>
        <li :class="{ 'loaded-flag': isLanguageLoaded('it') }"
            @click="changeLanguage('it')"
        >
          <img src="@/assets/it-flag.png"
               alt="Italian Flag"
               class="flag"
          >
        </li>
        <li :class="{ 'loaded-flag': isLanguageLoaded('jp') }"
            @click="changeLanguage('jp')"
        >
          <img src="@/assets/jp-flag.png"
               alt="Japanese Flag"
               class="flag"
          >
        </li>
      </ul>

      <ul v-if="isMenuOpen && canChangeTheme"
          class="themeMenu"
      >
        <li @click="addUCATheme()">
          <img src="@/assets/UCAthemeIcon.png"
               alt="Icon for UCA Theme"
               class="flag"
          >
        </li>
        <li @click="addDarkTheme()">
          <img src="@/assets/darkModeIcon.png"
               alt="Icon for Dark Theme"
               class="flag"
          >
        </li>
        <li @click="addTchooTheme()">
          <img src="@/assets/logo.png"
               alt="Icon for Tchoo Theme"
               class="flag"
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
*{
  transition: 500ms;
}
.gearDiv {
  position: fixed;
  width: 50px;
  height: 50px;
  right: 40px;
  bottom: 20px;
}

.gear {
  color: var(--white);
  width: 50px;
  height: 50px;
  transition: transform 0.3s ease;
}

.gearDiv:hover .gear {
  transform: rotate(-90deg);
}

.flagMenu {
  list-style-type: none;
  padding: 5px;
  margin: 0;
  position: absolute;
  bottom: 0;
  right: 50px;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.themeMenu {
  list-style-type: none;
  padding: 5px;
  margin: 0;
  position: absolute;
  bottom: 45px;
  right: 5px;
  display: flex;
  flex-direction: column-reverse;
  justify-content: center;
}

.flagMenu li {
  margin-right: 10px;
  cursor: pointer;
  padding-top: 20px;
}

.flagMenu li:nth-child(1) {
  padding-left: 10px;
}

.themeMenu li {
  margin-bottom: 5px;
  cursor: pointer;
  padding-left: 10px;
}

.flag {
  width: 30px;
  height: auto;
}

.loaded-flag .flag {
  /* Style pour les drapeaux chargés */
  border: 2px solid green;
  /* Ajoute d'autres styles selon tes besoins */
}

/* Styles pour les écrans plus petits */
@media (max-width: 600px) {
  .gearDiv {
    right: 20px;
  }

  .flags {
    width: 20px;
    height: auto;
  }

  .flagMenu li {
    margin-right: 5px;
  }
}
</style>
