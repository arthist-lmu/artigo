<template>
  <v-app id="app">
    <NavBar />
    <AppBar />

    <v-main class="mx-6 mb-6">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';
import NavBar from '@/components/NavBar.vue';

export default {
  components: {
    NavBar,
    AppBar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f9f9f9;
}
</style>
