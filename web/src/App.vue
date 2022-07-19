<template>
  <v-app
    id="app"
    :class="{ 'dark-variant': isDark }"
  >
    <Header :dark="isDark" />

    <Loader />
    <Toaster />

    <ResourceDialog />
    <ReconcileDialog />
    <GameSelectDialog />

    <v-main class="mx-6 mb-6">
      <router-view />
    </v-main>

    <Footer :dark="isDark" />
  </v-app>
</template>

<script>
export default {
  computed: {
    locale() {
      return this.$i18n.locale;
    },
    isDark() {
      const pages = ['home', 'about'];
      return pages.includes(this.$route.name);
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
