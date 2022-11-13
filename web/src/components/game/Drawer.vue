<template>
  <v-navigation-drawer
    v-model="drawer"
    :permanent="isPermanent"
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
            {{ $t("game.fields.new-game-default") }}
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
    value: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      drawer: false,
      width: 350,
    };
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
    isPermanent() {
      return this.$vuetify.breakpoint.mdAndUp;
    },
  },
  watch: {
    value() {
      this.drawer = this.value;
    },
    drawer(value) {
      this.$emit('input', value);
    },
    isPermanent(value) {
      this.$emit('input', !value);
    },
  },
  mounted() {
    this.$store.dispatch('statistics/get').then(() => {
      const params = { lang: this.$i18n.locale };
      this.$store.dispatch('home/get', params);
    });
  },
  components: {
    Card: () => import('./DrawerCard.vue'),
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
