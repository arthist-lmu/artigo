<template>
  <v-app-bar
    :style="getCss"
    :height="height"
    class="search"
    fixed
    flat
    app
  >
    <v-container class="mt-4">
      <v-row>
        <v-col class="pb-0">
          <slot>
            <DefaultBar
              :store="store"
              :filter="filter"
            />
          </slot>
        </v-col>
      </v-row>

      <slot name="append-item">

      </slot>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    store: {
      type: String,
      required: true,
    },
    height: {
      type: Number,
      required: false,
      default: 114,
    },
    filter: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    getCss() {
      const header = document.querySelector('header');
      return {
        'margin-top': `${header.offsetHeight}px`,
      };
    },
  },
  components: {
    DefaultBar: () => import('@/components/utils/DefaultBar.vue'),
  },
};
</script>

<style scoped>
.row.aggregate + .row.aggregate {
  margin-top: 0;
}
</style>
