<template>
  <v-navigation-drawer
    class="pl-2"
    color="transparent"
    width="400"
    clipped
    app
  >
    <v-img
      @click="goTo('home')"
      src="/assets/images/logo.svg"
      class="mx-8 mb-4"
      style="cursor: pointer;"
      max-width="250"
    />

    <v-list
      dense
      flat
    >
      <v-list-item
        v-for="page in pages"
        :key="page"
        dense
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-btn
              @click="goTo(page)"
              text
            >
              {{ $t(page)["title"] }}
            </v-btn>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <NavBarGame v-if="page === 'game'" />
    <NavBarGeneral v-else />
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      pages: [
        'about',
        'highscore',
      ],
    };
  },
  methods: {
    goTo(page, query) {
      this.$router.push({ name: page, query });
    },
  },
  computed: {
    page() {
      return this.$route.name;
    },
  },
  components: {
    NavBarGame: () => import('@/components/NavBarGame.vue'),
    NavBarGeneral: () => import('@/components/NavBarGeneral.vue'),
  },
};
</script>

<style>
.v-navigation-drawer__border {
  display: none;
}
</style>

<style scoped>
.v-navigation-drawer {
  background-color: transparent;
}

.v-list-item__content {
  padding: 0 !important;
}
</style>
