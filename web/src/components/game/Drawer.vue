<template>
  <v-navigation-drawer
    :width="width"
    app
  >
    <v-container class="px-6">
      <v-row></v-row>

      <v-row
        v-for="entry in data"
        :key="entry.path"
        style="flex: 0;"
      >
        <v-col>
          <Card :entry="entry" />
        </v-col>
      </v-row>

      <v-row style="flex: 0;">
        <v-col>
          <v-btn
            @click="goTo('game')"
            color="grey lighten-2"
            depressed
            outlined
            rounded
            block
          >
            {{ $t("game.fields.new-game") }}
          </v-btn>
        </v-col>
      </v-row>

      <v-row></v-row>
    </v-container>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    width: {
      type: Number,
      default: 325,
    },
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
  },
  computed: {
    data() {
      return this.$store.state.home.data;
    },
  },
  mounted() {
    const params = { lang: this.$i18n.locale };
    this.$store.dispatch('home/get', params);
  },
  components: {
    Card: () => import('./Card.vue'),
  },
};
</script>

<style scoped>
.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}
</style>
