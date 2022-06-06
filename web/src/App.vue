<template>
  <v-app id="app">
    <NavBar />
    <AppBar />
    <Loader />
    <Toaster />

    <ResourceDialog />
    <ReconcileDialog />

    <v-main class="mx-6 mb-6">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  computed: {
    locale() {
      return this.$i18n.locale;
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
    NavBar: () => import('@/components/NavBar.vue'),
    AppBar: () => import('@/components/AppBar.vue'),
    Loader: () => import('@/components/Loader.vue'),
    Toaster: () => import('@/components/Toaster.vue'),
    ResourceDialog: () => import('@/components/ResourceDialog.vue'),
    ReconcileDialog: () => import('@/components/ReconcileDialog.vue'),
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f9f9f9;
}
</style>
