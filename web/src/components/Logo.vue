<template>
  <div style="display: contents;">
    <img
      @click="goToHome"
      @keydown="goToHome"
      alt="ARTigo – Social Image Tagging"
      src="/assets/images/logo.svg"
      :class="{ dark: dark }"
      style="cursor: pointer;"
      height="32"
    />

    <GameMenu :dark="dark" />
  </div>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    goToHome() {
      this.$router.push({ name: 'home' });
    },
  },
  components: {
    GameMenu: () => import('@/components/game/Menu.vue'),
  },
};
</script>

<style scoped>
img.dark {
  filter: brightness(0) saturate(100%) invert(99%) sepia(1%) saturate(485%) hue-rotate(184deg) brightness(99%) contrast(99%);
}
</style>
