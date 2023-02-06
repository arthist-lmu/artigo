<template>
  <v-app-bar
    v-if="isVisible"
    :style="{ left: `${left}px !important` }"
    :dark="dark"
    clipped-left
    flat
    app
  >
    <v-container :class="{ opaque: opaque }">
      <v-row
        align="center"
        no-gutters
      >
        <Logo :dark="dark" />

        <v-spacer />

        <v-col
          v-if="!(true || hideSearchBar || $vuetify.breakpoint.mobile)"
          cols="4"
        >
          <Bar />
        </v-col>

        <v-col
          cols="4"
          align="right"
        >
          <MobileMenu
            v-if="$vuetify.breakpoint.mobile"
            :dark="dark"
          />
          <DefaultMenu
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
    opaque: {
      type: Boolean,
      default: false,
    },
    hideSearchBar: {
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
      return this.$store.state.utils.drawer.width;
    },
    isVisible() {
      if (
        this.$route.name !== 'game'
        || this.$vuetify.breakpoint.smAndUp
      ) {
        return true;
      }
      return !this.$store.state.game.input.focus;
    },
  },
  mounted() {
    this.$emit('mounted');
  },
  components: {
    Bar: () => import('@/components/search/Bar.vue'),
    Logo: () => import('@/components/Logo.vue'),
    DefaultMenu: () => import('@/components/menu/Default.vue'),
    MobileMenu: () => import('@/components/menu/Mobile.vue'),
    UserMenu: () => import('@/components/account/Menu.vue'),
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

.v-app-bar .container.opaque {
  opacity: 0.25;
}

.v-app-bar .container:hover {
  opacity: 1;
}
</style>
