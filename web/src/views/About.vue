<template>
  <v-container>
    <GameDrawer />

    <v-row
      v-if="!$vuetify.breakpoint.mdAndDown"
      ref="filler"
    />

    <v-row ref="summary">
      <v-col :class="$vuetify.breakpoint.mdAndDown ? 'px-1 py-6' : 'pa-12'">
        <div :class="[$vuetify.breakpoint.mdAndDown ? 'text-h3' : 'text-h2', 'accent--text']">
          {{ $t("about.fields.summary", { images, taggings, users }) }}
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="$vuetify.breakpoint.mdAndDown ? 'px-1 py-6' : 'pa-12'">
        <div :class="[$vuetify.breakpoint.mdAndDown ? 'text-h3' : 'text-h2', 'accent--text mb-6']">
          {{ $t("contributors.title") }}
        </div>

        <Contributors />
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="$vuetify.breakpoint.mdAndDown ? 'px-1 py-6' : 'pa-12'">
        <div :class="[$vuetify.breakpoint.mdAndDown ? 'text-h3' : 'text-h2', 'accent--text mb-6']">
          {{ $t("publications.title") }}
        </div>

        <Publications />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  computed: {
    data() {
      return this.$store.state.statistics.data;
    },
    lang() {
      return this.$i18n.locale;
    },
    users() {
      if (this.keyInObj('users', this.data)) {
        const { n } = this.data.users;
        return n.toLocaleString(this.lang);
      }
      return 0;
    },
    images() {
      if (this.keyInObj('resources', this.data)) {
        const { n } = this.data.resources;
        return n.toLocaleString(this.lang);
      }
      return 0;
    },
    taggings() {
      if (this.keyInObj('taggings', this.data)) {
        const { n } = this.data.taggings;
        return n.toLocaleString(this.lang);
      }
      return 0;
    },
  },
  mounted() {
    this.$store.dispatch('statistics/get');
    window.scrollTo(0, 0);
  },
  components: {
    GameDrawer: () => import('@/components/game/Drawer.vue'),
    Contributors: () => import('@/components/Contributors.vue'),
    Publications: () => import('@/components/Publications.vue'),
  },
};
</script>

<style scoped>
.text-h2 {
  line-height: 4.75rem;
}

.text-h3 {
  line-height: 3.75rem;
}
</style>
