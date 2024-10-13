<template>
  <div style="position: relative;">
    <img
      alt="ARTigo – Social Image Tagging"
      src="/assets/images/logo.svg"
      height="32"
      @click="goTo('home')"
      @keydown="goTo('home')"
    >

    <GameMenu />
  </div>
</template>

<script setup>
import GameMenu from '@/components/menu/GameMenu.vue'
import goTo from '@/composables/useGoTo'
</script>

<style scoped>
img {
  cursor: pointer;
}

.v-theme--dark img {
  filter: brightness(0) saturate(100%) invert(99%) sepia(1%) saturate(485%) hue-rotate(184deg) brightness(99%) contrast(99%);
  display: flex;
}
</style>
