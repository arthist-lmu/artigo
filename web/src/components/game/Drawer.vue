<template>
  <v-navigation-drawer
    v-model="drawer"
    :permanent="isPermanent"
    :width="width"
    app
  >
    <v-container class="px-6">
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
    get(name = null) {
      this.$store.dispatch('statistics/get').then(() => {
        const params = { lang: this.$i18n.locale, name };
        this.$store.dispatch('home/get', params);
      });
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
    '$route.query.collection'(name) {
      this.get(name);
    },
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
    this.get(this.$route.query.collection);
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

.row:nth-last-child(2) {
  padding-bottom: 12px;
}
</style>
