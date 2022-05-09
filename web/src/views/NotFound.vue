<template>
  <div
    class="logo"
    @click="reset"
    @keyDown="handleReset"
    style="cursor: pointer"
  >
    <h1>404 Not found</h1>

    <img
      src="/assets/images/logo.svg"
      alt=""
    />
  </div>
</template>

<script>
export default {
  methods: {
    reset() {
      this.$router.push('/');
    },
    handleReset(evt) {
      if (evt.keyCode === 13) {
        reset();
      }
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

#not-found .logo > img {
  max-height: 56px;
}
</style>
