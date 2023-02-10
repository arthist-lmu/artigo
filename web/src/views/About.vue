<template>
  <v-container>
    <GameDrawer />

    <v-row ref="summary">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("about.fields.summary", { images, taggings, users }) }}
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="paddingClass">
        <Description />
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("contributors.title") }}
        </div>

        <Contributors />
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("history.title") }}
        </div>

        <History />
      </v-col>
    </v-row>

    <v-row>
      <v-col :class="paddingClass">
        <div :class="textClass">
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
    textClass() {
      const values = ['accent--text', 'mb-6'];
      switch (this.$vuetify.breakpoint.name) {
        case 'xs':
          values.push('text-h4');
          break;
        case 'sm':
          values.push('text-h3');
          break;
        default:
          values.push('text-h2');
          break;
      }
      return values;
    },
    paddingClass() {
      if (this.$vuetify.breakpoint.mdAndDown) {
        return ['px-1', 'py-6'];
      }
      return ['pa-12'];
    },
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
    // see: @/components/game/Drawer.vue
    // this.$store.dispatch('statistics/get');
    window.scrollTo(0, 0);
  },
  components: {
    GameDrawer: () => import('@/components/game/Drawer.vue'),
    Description: () => import('@/components/Description.vue'),
    Contributors: () => import('@/components/Contributors.vue'),
    History: () => import('@/components/History.vue'),
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

.text-h4 {
  line-height: 2.75rem;
}
</style>
