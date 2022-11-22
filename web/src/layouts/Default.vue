<template>
  <v-app
    id="app"
    :class="{ 'dark-variant': dark }"
  >
    <Header
      :dark="dark"
      :opaque="opaque"
      @mounted="mounted = true;"
    />

    <Loader />
    <Toaster />

    <ResourceDialog />
    <ReconcileDialog />
    <GameSelectDialog />

    <v-main
      v-if="mounted"
      class="mx-6 mb-6"
    >
      <slot />
    </v-main>

    <Footer
      :dark="dark"
      :opaque="opaque"
    />
  </v-app>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    opaque: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      mounted: false,
    };
  },
  components: {
    Header: () => import('@/components/Header.vue'),
    Loader: () => import('@/components/Loader.vue'),
    Toaster: () => import('@/components/Toaster.vue'),
    Footer: () => import('@/components/Footer.vue'),
    ResourceDialog: () => import('@/components/ResourceDialog.vue'),
    ReconcileDialog: () => import('@/components/ReconcileDialog.vue'),
    GameSelectDialog: () => import('@/components/game/SelectDialog.vue'),
  },
};
</script>

<style scoped>
.theme--light.dark-variant.v-application {
  background-color: rgb(66, 71, 152);
}
</style>
