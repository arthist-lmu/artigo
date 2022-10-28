<template>
  <v-combobox
    v-model="query"
    ref="input"
    @click:prepend-inner="onButton"
    @keyup.enter.native="search"
    :placeholder="$t('sessions.fields.query')"
    prepend-inner-icon="mdi-magnify"
    hide-details
    rounded
    solo
    flat
  >
    <template v-slot:no-data>

    </template>

    <template v-slot:append>
      <template v-if="total > 0">
        <v-divider
          class="mx-4"
          vertical
        />

        <span>
          <v-btn
            @click.stop="previousPage"
            class="mr-1"
            :disabled="page <= 1"
            icon
          >
            <v-icon>
              mdi-chevron-left
            </v-icon>
          </v-btn>

          <span
            v-if="!$vuetify.breakpoint.mdAndDown"
            class="mr-1"
          >
            {{ offset + 1 }}–{{ offset + entries.length }}
            {{ $t('sessions.fields.of') }} {{ total }}
          </span>

          <v-btn
            @click.stop="nextPage"
            class="ml-1 mr-n3"
            :disabled="page >= numberOfPages"
            icon
          >
            <v-icon>
              mdi-chevron-right
            </v-icon>
          </v-btn>
        </span>
      </template>
    </template>
  </v-combobox>
</template>

<script>
export default {
  data() {
    return {
      page: 1,
      query: null,
    };
  },
  methods: {
    search() {
      this.$store.dispatch('sessions/get', { 'query': this.query });
    },
    onButton() {
      this.blurInput();
      this.$nextTick(() => {
        this.search();
      });
    },
    blurInput() {
      if (this.$refs.input !== undefined) {
        this.$refs.input.blur();
      }
    },
    nextPage() {
      this.page += 1;
    },
    previousPage() {
      this.page -= 1;
    },
  },
  computed: {
    total() {
      return this.$store.state.sessions.data.total;
    },
    offset() {
      return this.$store.state.sessions.data.offset;
    },
    entries() {
      return this.$store.state.sessions.data.entries;
    },
    itemsPerPage() {
      return this.$store.state.sessions.itemsPerPage;
    },
    numberOfPages() {
      return Math.ceil(this.total / this.itemsPerPage);
    },
  },
  watch: {
    page(value) {
      const lastEntry = this.entries.length + this.offset;
      const withLastEntry = this.total === lastEntry;
      if (
        ((value * this.itemsPerPage > lastEntry) && !withLastEntry)
        || (value * this.itemsPerPage <= this.offset)
      ) {
        const offset = (value - 1) * this.itemsPerPage;
        this.$store.dispatch('sessions/get', { offset });
      }
    },
    entries() {
      window.scrollTo(0, 0);
    },
  },
};
</script>

<style scoped>
.v-list {
  padding: 0;
}
</style>
