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
        <v-col class="pb-3">
          <Bar />
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      height: 112,
    };
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
    Bar: () => import('@/components/session/Bar.vue'),
  },
};
</script>
