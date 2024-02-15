<script>
export default {
  name: 'ClearButtonSelector',

  props: {
    // eslint-disable-next-line vue/no-unused-properties
    isSelect: {
      type: Boolean,
      default: false,
    },
    /* eslint-enable */
    styleUnselect: {
      type: String,
      default: "unselect",
    },
    styleSelect: {
      type: String,
      default: "select",
    },
  },
  emits: ["clicked"],
  data() {
    return {
      style: this.styleUnselect,
    };
  },
  methods: {
    changeStyle() {
      if (this.style === this.styleUnselect) {
        this.style = this.styleSelect;
        this.isSelect = false;
      } else {
        this.style = this.styleUnselect;
        this.isSelect = true;
      }
    },
    getState() {
      return this.isSelect;
    },
  },
}
</script>

<template>
  <a :class="style"
     @click="changeStyle"
  >
    <slot />
  </a>
</template>

<style scoped>

.unselect {
  border-radius: 20px;
  border: 1px solid var(--CTA-color);
  background-color: white;
  padding: 0.5em 2em;
  text-decoration: none;
  color: var(--text-color);
  font-family: "Sofia Sans", sans-serif;

  cursor: pointer;
  user-select: none;
}

.select {
  border-radius: 20px;
  border: 1px solid var(--CTA-color);
  background-color: var(--CTA-color);
  padding: 0.5em 2em;
  text-decoration: none;
  color: var(--white);
  font-family: "Sofia Sans", sans-serif;

  cursor: pointer;
  user-select: none;
}


</style>