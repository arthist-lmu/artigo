<template>
  <v-app-bar
    :style="getCss"
    :dark="dark"
    clipped-left
    flat
    app
  >
    <v-container :class="{ transparent: hasOpacity }">
      <v-row
        align="center"
        no-gutters
      >
        <img
          @click="goTo('home')"
          @keydown="goTo('home')"
          alt="ARTigo – Social Image Tagging"
          src="/assets/images/logo.svg"
          :class="{ dark: dark }"
          style="cursor: pointer;"
          height="36"
        />

        <GameMenu :dark="dark" />

        <v-spacer />

        <v-col
          v-if="!(dark || isMobile || isSearch)"
          cols="4"
        >
          <SearchBar />
        </v-col>

        <v-col
          cols="4"
          align="right"
        >
          <MobileMenu
            v-if="isMobile"
            :dark="dark"
          />
          <DesktopMenu
            v-else
            :dark="dark"
          />

          <UserMenu :dark="dark" />
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
  },
  computed: {
    left() {
      if (this.$vuetify.breakpoint.lgAndUp) {
        return this.$store.state.utils.drawer.width;
      }
      return 0;
    },
    getCss() {
      return { left: `${this.left}px !important` };
    },
    isSearch() {
      return this.$route.name === 'search';
    },
    isMobile() {
      return this.$vuetify.breakpoint.mobile;
    },
    hasOpacity() {
      return ['game', 'session'].includes(this.$route.name);
    },
  },
  components: {
    SearchBar: () => import('@/components/SearchBar.vue'),
    MobileMenu: () => import('@/components/MobileMenu.vue'),
    DesktopMenu: () => import('@/components/DesktopMenu.vue'),
    GameMenu: () => import('@/components/game/Menu.vue'),
    UserMenu: () => import('@/components/UserMenu.vue'),
  },
};
</script>

<style scoped>
.v-app-bar .container {
  z-index: 99;
  transition: opacity .5s ease-out;
  -moz-transition: opacity .5s ease-out;
  -webkit-transition: opacity .5s ease-out;
  -o-transition: opacity .5s ease-out;
}

.v-app-bar .container.transparent {
  opacity: 0.25;
}

.v-app-bar .container:hover {
  opacity: 1;
}

img.dark {
  filter: brightness(0) saturate(100%) invert(99%) sepia(1%) saturate(485%) hue-rotate(184deg) brightness(99%) contrast(99%);
}
</style>
