<template>
  <v-data-iterator
    :items="entries"
    :items-per-page.sync="itemsPerPage"
    :page.sync="page"
    hide-default-footer
  >
    <template v-slot:default="props">
      <v-row :class="{ 'ma-n1': $vuetify.breakpoint.mdAndUp }">
        <v-col
          v-for="entry in props.items"
          :key="entry.resource_id"
          :cols="(12 / itemsPerRow)"
          class="pa-1"
        >
          <component
            :is="component"
            :entry="entry"
          />
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
            {{ $t(`${store}.fields.no-results`) }}
          </v-alert>
        </v-col>
      </v-row>
    </template>
  </v-data-iterator>
</template>

<script>
export default {
  props: {
    component: {
      required: true,
    },
    store: {
      type: String,
      required: true,
    },
    reload: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  data() {
    return {
      page: 1,
      checkInterval: null,
    };
  },
  computed: {
    entries() {
      return this.$store.state[this.store].data.entries;
    },
    itemsPerPage() {
      return this.$store.state[this.store].itemsPerPage;
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
  watch: {
    entries() {
      clearInterval(this.checkInterval);
      if (this.reload) {
        this.checkInterval = setInterval(() => {
          this.$store.dispatch(`${this.store}/post`, {});
        }, 10 * 1000);
      }
    },
  },
  beforeDestroy() {
    clearInterval(this.checkInterval);
  },
  mounted() {
    window.scrollTo(0, 0);
  },
  created() {
    this.$store.dispatch(`${this.store}/post`, {});
  },
};
</script>

<style>
.v-data-iterator > div:not(.row) {
  height: 100%;
}
</style>

<style scoped>
.row.justify-center {
  height: 100%;
}
</style>
