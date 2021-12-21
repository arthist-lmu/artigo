<template>
  <v-app id="app">
    <NavBar />
    <AppBar />

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 10px;
}
</style>

<script>
import AppBar from "@/components/AppBar.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  created() {
    document.title = "ARTigo - Social Image Tagging";
  },
  components: {
    NavBar,
    AppBar,
  },
  data() {
    return {};
  },
};
</script>
