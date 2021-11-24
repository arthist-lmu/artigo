<template>
  <div id="app">

      <button
      class="btn btn-primary btn-margin"
      v-if="!authenticated"
      @click="login()">
      Log In

    </button>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
