<template>
  <v-app
    id="app"
    :class="{ 'dark-variant': isHome }"
  >
    <Header
      :dark="isHome"
      :left="width"
    />
    <GameDrawer
      v-if="isHome"
      :width="width"
    />

    <Loader />
    <Toaster />

    <ResourceDialog />
    <ReconcileDialog />
    <GameSelectDialog />

    <v-main class="mx-6 mb-6">
      <router-view />
    </v-main>

    <Footer :dark="isHome" />
  </v-app>
</template>

<script>
export default {
  computed: {
    width() {
      return this.isHome ? 300 : 0;
    },
    locale() {
      return this.$i18n.locale;
    },
    isHome() {
      return this.$route.name === 'home';
    },
  },
  watch: {
    locale(lang) {
      const { query } = this.$route;
      this.$router.push({ params: { lang }, query });
      document.documentElement.lang = lang;
    },
  },
  created() {
    document.documentElement.lang = this.locale;
  },
  components: {
    Header: () => import('@/components/Header.vue'),
    Loader: () => import('@/components/Loader.vue'),
    Toaster: () => import('@/components/Toaster.vue'),
    Footer: () => import('@/components/Footer.vue'),
    GameDrawer: () => import('@/components/game/Drawer.vue'),
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
