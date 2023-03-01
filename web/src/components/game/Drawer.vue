<template>
  <v-navigation-drawer
    v-model="drawer"
    :permanent="isPermanent"
    :width="width"
    app
  >
    <v-container class="pb-8 px-6">
      <v-row class="ma-0" />

      <v-row
        v-for="entry in data"
        :key="entry.path"
        style="flex: 0;"
      >
        <v-col>
          <Card :entry="entry" />
        </v-col>
      </v-row>

      <v-row
        class="pb-4"
        style="flex: 0;"
      >
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

      <v-row class="ma-0" />
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
    width() {
      // see: @/components/Footer.vue for change
      return this.isPermanent ? 350 : 300;
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

.row:first-child + .row {
  margin-top: 0;
}
</style>
