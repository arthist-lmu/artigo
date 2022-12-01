<template>
  <v-container class="pt-0">
    <Bar />

    <v-data-iterator
      :items="entries"
      :items-per-page.sync="itemsPerPage"
      :page.sync="page"
      hide-default-footer
    >
      <template v-slot:default="props">
        <v-row :class="$vuetify.breakpoint.mdAndUp ? 'ma-n1' : undefined">
          <v-col
            v-for="entry in props.items"
            :key="entry.resource_id"
            :cols="(12 / itemsPerRow)"
            class="pa-1"
          >
            <ResultCard :entry="entry" />
          </v-col>
        </v-row>
      </template>

      <template v-slot:no-data>
        <v-row justify="center">
          <v-col
            :cols="noDataCols"
            align-self="center"
          >
            <v-alert
              class="mb-0"
              type="error"
              icon="mdi-alert-circle-outline"
              colored-border
            >
              {{ $t("sessions.fields.no-results") }}
            </v-alert>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      page: 1,
    };
  },
  computed: {
    entries() {
      return this.$store.state.sessions.data.entries;
    },
    itemsPerPage() {
      return this.$store.state.sessions.itemsPerPage;
    },
    itemsPerRow() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 1;
        case 'sm': return 2;
        case 'md': return 3;
        case 'lg': return 4;
        default: return 6;
      }
    },
    noDataCols() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 12;
        case 'sm': return 9;
        case 'md': return 6;
        case 'lg': return 4;
        default: return 3;
      }
    },
  },
  created() {
    this.$store.dispatch('sessions/get', {});
  },
  components: {
    Bar: () => import('@/components/session/ExtendedBar.vue'),
    ResultCard: () => import('@/components/session/Card.vue'),
  },
};
</script>

<style>
.v-data-iterator > div:not(.row) {
  height: 100%;
}
</style>

<style scoped>
.container,
.container > div,
.container .justify-center {
  height: 100%;
}

.row > .col:empty {
  display: none;
}
</style>
