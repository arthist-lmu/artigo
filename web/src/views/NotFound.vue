<template>
  <v-app id="not-found">
    <div
      class="logo"
      @click="reset"
      style="cursor: pointer;"
    >
      <h1> 404 Not found </h1>
      <img src="/assets/images/logo.png" />
    </div>
  </v-app>
</template>

<script>
export default {
  methods: {
    reset() {
      this.$router.push('/');
    },
  },
};
</script>

<style>
#not-found {
  justify-content: center;
  align-items: center;
  display: flex;
  height: 100%;
}

#not-found .logo {
  margin: auto;
}

#not-found .logo>img {
  max-height: 56px;
}
</style>
