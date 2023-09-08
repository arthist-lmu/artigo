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

        <DefaultMenu
          v-if="!$vuetify.breakpoint.mobile"
          :dark="dark"
        />

        <v-btn
          v-if="!hideSearchBar"
          @click="goTo('search')"
          :title="$t('search.title')"
          class="ml-2"
          :color="dark ? 'accent' : 'primary'"
          :dark="dark"
          icon
        >
          <v-icon>
            mdi-magnify
          </v-icon>
        </v-btn>

        <UserMenu :dark="dark" />
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
    Logo: () => import('@/components/Logo.vue'),
    DefaultMenu: () => import('@/components/menu/Default.vue'),
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
