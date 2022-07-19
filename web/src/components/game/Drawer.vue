<template>
  <v-navigation-drawer
    v-model="drawer"
    :temporary="isTemporary"
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
    forceOpen: {
      type: Boolean,
      default: false,
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
    isTemporary() {
      return !this.$vuetify.breakpoint.lgAndUp;
    },
  },
  watch: {
    drawer: {
      handler(value) {
        const params = { width: 0 };
        if (value) params.width = this.width;
        this.$store.commit('utils/updateDrawer', params);
      },
      immediate: true,
    },
    forceOpen: {
      handler(value) {
        if (value) {
          this.drawer = true;
        }
      },
      immediate: true,
    },
    isTemporary: {
      handler(value) {
        this.drawer = !value;
      },
      immediate: true,
    },
  },
  mounted() {
    const params = { lang: this.$i18n.locale };
    this.$store.dispatch('home/get', params);
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
