<template>
  <v-app-bar
    :style="getCss"
    :height="height"
    fixed
    flat
    app
  >
    <v-container>
      <v-row>
        <v-col class="pb-0">
          <Bar :dense="false" />
        </v-col>
      </v-row>

      <v-row
        v-for="aggregation in aggregations"
        :key="aggregation.field"
        class="aggregate"
      >
        <v-col v-if="aggregation.entries.length">
          <v-slide-group show-arrows>
            <v-slide-item
              v-for="entry in aggregation.entries"
              :key="entry.name"
            >
              <v-chip
                @click="search(entry.name)"
                class="mx-1"
                depressed
                outlined
                rounded
              >
                {{ entry.name }}
              </v-chip>
            </v-slide-item>
          </v-slide-group>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  methods: {
    search(value) {
      const query = { tags: value };
      this.$store.dispatch('search/post', { query });
    },
  },
  computed: {
    aggregations() {
      return this.$store.state.search.data.aggregations;
    },
    height() {
      let height = 100;
      if (this.aggregations.length) {
        this.aggregations.forEach((aggregation) => {
          if (aggregation.entries.length) {
            height += 56;
          }
        });
      }
      return height;
    },
    getCss() {
      const header = document.querySelector('header');
      return {
        'margin-top': `${header.offsetHeight}px`,
      };
    },
  },
  components: {
    Bar: () => import('@/components/search/Bar.vue'),
  },
};
</script>

<style scoped>
.row.aggregate + .row.aggregate {
  margin-top: 0;
}
</style>
