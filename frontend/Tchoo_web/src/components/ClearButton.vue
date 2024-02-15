<script setup>
const props = defineProps({
  /* eslint-disable */
    to: {
        type: String,
        required: true
    }
  /* eslint-enable */
})
</script>

<template>
  <router-link :to="props.to">
    <slot />
  </router-link>
</template>

<style scoped>
a {
    border-radius: 20px;
    border: 1px solid var(--main-color);
    background-color: var(--white);
    padding: 10px 2em;
    text-decoration: none;
    color: var(--text-color);
    font-family: "Sofia Sans", sans-serif;
    transition: 500ms;
}

a:hover {
    cursor: pointer;
    background-color: var(--CTA-color);
    color: white;
    transition: 700ms;
}
</style>