<script>
import ArrowButton from "@/components/icons/ArrowButton.svg"
import ArrowButtonFull from "@/components/icons/ArrowButtonFull.svg"

export default {
  name: 'ArrowButton',
  props: {
    originalSrc: {
      type: String,
      default: ArrowButton,
    },
    hoverSrc: {
      type: String,
      default: ArrowButtonFull,
    },
    rotation: {
      type: Number,
      default: 0,
    },
    active: {
      type: Boolean,
      required: true
    }
  },
  emits: ["clicked"],
  data() {
    return {
      selected: false,
      currentSrc: this.originalSrc,
    };
  },
  methods: {
    changeImageSrc() {
      if (!this.active) return;

      if (this.currentSrc === this.originalSrc) {
        this.currentSrc = this.hoverSrc;
        this.selected = true;
      } else {
        this.currentSrc = this.originalSrc;
        this.selected = false;
      }

      this.$emit('clicked', this.selected)
    },
  }
}
</script>

<template>
  <div :class="active ? '' : 'inactive'">
    <img
      class="answer-arrow"
      :src="currentSrc"
      :style="{transform: `rotate(${rotation}deg)`, width: '90%', height: '90%', objectFit: 'fill', color: 'white', padding: `${padding}px`}"
      alt="Arrow"
      @click="changeImageSrc()"
    >
  </div>
</template>

<style>

.answer-arrow {
  filter: var(--filter);
}

.answer-arrow:hover {
  cursor: pointer;
}

.inactive .answer-arrow:hover {
  cursor: not-allowed;
}
</style>
