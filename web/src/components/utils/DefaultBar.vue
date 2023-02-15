<template>
  <v-combobox
    v-model="query['all-text']"
    ref="input"
    @click:prepend-inner="onButton"
    @keyup.enter.native="search"
    :placeholder="$t(`${store}.fields.query`)"
    prepend-inner-icon="mdi-magnify"
    :menu-props="{ maxHeight: 400, value: openMenu }"
    hide-details
    rounded
    solo
    flat
  >
    <template v-slot:no-data>
      <v-container
        v-click-outside="onClickOutside"
        class="pa-8"
      >
        <v-row
          v-for="item in items"
          :key="item.key"
          class="mb-2"
        >
          <v-combobox
            v-model="query[item.key]"
            :ref="item.key"
            :placeholder="$t('resource.metadata.fields')[item.key]"
            append-icon=""
            hide-details
            single-line
            outlined
            multiple
            rounded
            dense
            chips
          >
            <template v-slot:selection="{ attrs, item, selected }">
              <v-chip
                v-bind="attrs"
                :input-value="selected"
                color="primary"
                outlined
                close
                small
              >
                {{ item }}
              </v-chip>
            </template>
          </v-combobox>
        </v-row>

        <v-row>
          <v-col
            class="pa-0 pt-2"
            align="right"
          >
            <v-btn
              @click="search"
              color="primary"
              depressed
              rounded
            >
              {{ $t('search.title') }}
            </v-btn>

            <v-btn
              @click="reset"
              :title="$t('search.fields.reset')"
              color="grey"
              class="ml-2"
              icon
            >
              <v-icon>mdi-restore</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>

    <template v-slot:append>
      <template v-if="filter">
        <v-badge
          v-if="numberOfQueries > 0"
          :content="numberOfQueries"
          inline
        >
          <v-btn
            @click="toggle"
            icon
          >
            <v-icon>
              mdi-tune-variant
            </v-icon>
          </v-btn>
        </v-badge>
        <v-btn
          v-else
          @click="toggle"
          icon
        >
          <v-icon>
            mdi-tune-variant
          </v-icon>
        </v-btn>
      </template>
      <template v-else>
        <v-btn
          v-if="query['hide-empty']"
          :title="$t(`${store}.fields.show-empty`)"
          @click="hideEmpty"
          icon
        >
          <v-icon>
            mdi-flask-empty-plus-outline
          </v-icon>
        </v-btn>
        <v-btn
          v-else
          :title="$t(`${store}.fields.hide-empty`)"
          @click="hideEmpty"
          icon
        >
          <v-icon>
            mdi-flask-empty-minus-outline
          </v-icon>
        </v-btn>
      </template>

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
            v-if="!$vuetify.breakpoint.smAndDown"
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
  props: {
    store: {
      type: String,
      required: true,
    },
    filter: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      page: 1,
      query: {},
      openMenu: false,
      items: [
        { key: 'titles' },
        { key: 'creators' },
        { key: 'location' },
        { key: 'institution' },
        { key: 'tags' },
      ],
    };
  },
  methods: {
    reset() {
      this.query = {};
    },
    toggle() {
      this.openMenu = !this.openMenu;
    },
    search() {
      this.$store.dispatch(`${this.store}/post`, { 'query': this.query }).then(() => {
        this.closeMenu();
      });
    },
    hideEmpty() {
      this.query['hide-empty'] = !this.query['hide-empty'];
      this.search();
    },
    onButton() {
      this.blurInput();
      this.$nextTick(() => {
        this.search();
      });
    },
    onClickOutside({ target }) {
      if (this.$refs.input !== undefined) {
        const input = this.$refs.input.$el;
        if (!input.contains(target)) {
          this.closeMenu();
        }
      }
    },
    blurInput() {
      if (this.$refs.input !== undefined) {
        this.$refs.input.blur();
      }
    },
    closeMenu() {
      this.openMenu = false;
    },
    nextPage() {
      this.page += 1;
    },
    previousPage() {
      this.page -= 1;
    },
  },
  computed: {
    params() {
      return this.$store.state.search.params;
    },
    total() {
      return this.$store.state[this.store].data.total;
    },
    offset() {
      return this.$store.state[this.store].data.offset;
    },
    entries() {
      return this.$store.state[this.store].data.entries;
    },
    itemsPerPage() {
      return this.$store.state[this.store].itemsPerPage;
    },
    numberOfPages() {
      return Math.ceil(this.total / this.itemsPerPage);
    },
    numberOfQueries() {
      let counter = 0;
      Object.values(this.query).forEach((values) => {
        if (values instanceof Array) {
          counter += values.length;
        }
      });
      return counter;
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
        this.$store.dispatch(`${this.store}/post`, { offset });
      }
    },
    params: {
      handler({ query }) {
        this.query = { 'hide-empty': false };
        if (query) {
          Object.entries(query).forEach(([key, values]) => {
            if (!this.isArray(values)) {
              values = [values];
            }
            if (['all-text', 'hide-empty'].includes(key)) {
              [values] = values;
            }
            this.query[key] = values;
          });
        }
      },
      immediate: true,
    },
    entries() {
      window.scrollTo(0, 0);
    },
    openMenu(value) {
      if (value) {
        this.blurInput();
        setTimeout(() => {
          this.$nextTick(() => {
            this.$refs.titles[0].focus();
          });
        }, 250);
      }
    },
  },
};
</script>

<style scoped>
.v-list {
  padding: 0;
}
</style>
