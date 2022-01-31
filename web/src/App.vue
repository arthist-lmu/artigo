<template>
  <v-app id="app">
    <NavBar />
    <AppBar />
    <Loader />
    <Toaster />

    <v-main class="mx-6 mb-6">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';
import NavBar from '@/components/NavBar.vue';
import Loader from '@/components/Loader.vue';
import Toaster from '@/components/Toaster.vue';

export default {
  components: {
    NavBar,
    AppBar,
    Loader,
    Toaster,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f9f9f9;
}
</style>
