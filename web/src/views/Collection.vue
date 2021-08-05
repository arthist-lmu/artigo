<template>
  <v-app id="collection">
    <AppBar />

    <v-main>
      <v-container>
        {{ data }}
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '@/components/AppBar.vue';

export default {
  methods: {
    getData(name) {
      this.$store.dispatch('collection/get', { name });
    },
  },
  computed: {
    data() {
      return this.$store.state.collection.data;
    },
    title() {
      return this.capitalize(this.data.name);
    },
  },
  watch: {
    '$route.params.name': function (name) {
      this.getData(name);
    },
    data() {
      document.title = `${this.title} | ${APP_NAME}`;
    },
  },
  created() {
    this.getData(this.$route.params.name);
  },
  components: {
    AppBar,
  },
};
</script>

<style>
</style>
