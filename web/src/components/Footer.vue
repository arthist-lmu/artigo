<template>
  <v-footer
    v-if="isVisible"
    ref="footer"
    :dark="dark"
    :style="$vuetify.breakpoint.mdAndDown ? undefined : 'padding: 0 12px;'"
    padless
    fixed
    inset
    app
  >
    <v-container
      :class="{
        'px-7': $vuetify.breakpoint.smAndDown,
        opaque: opaque,
      }"
    >
      <v-row>
        <v-col
          :cols="$vuetify.breakpoint.mdAndDown ? '3' : '6'"
          align="left"
        >
          <v-btn
            @click="goTo('about')"
            :title="$t('about.title')"
            :color="dark ? 'accent' : 'primary'"
            depressed
            rounded
            :small="!$vuetify.breakpoint.mdAndDown"
            :x-small="$vuetify.breakpoint.mdAndDown"
          >
            <v-icon left>
              mdi-information-outline
            </v-icon>

            2010–{{ new Date().getFullYear() }}
          </v-btn>

          <v-chip
            v-if="!$vuetify.breakpoint.mdAndDown"
            @click="goTo('institute')"
            style="background-color: transparent;"
            class="ml-2"
            small
          >
            Ludwig-Maximilians-Universität München
          </v-chip>
        </v-col>

        <v-col
          :cols="$vuetify.breakpoint.mdAndDown ? '9' : '6'"
          align="right"
        >
          <v-btn
            v-if="!$vuetify.breakpoint.mdAndDown"
            :href="api"
            target="_blank"
            :small="!$vuetify.breakpoint.mdAndDown"
            :x-small="$vuetify.breakpoint.mdAndDown"
            icon
          >
            <v-icon>
              mdi-api
            </v-icon>
          </v-btn>

          <v-btn
            v-for="page in pages"
            :key="page"
            @click="goTo(page)"
            class="ml-2"
            color="grey lighten-2"
            outlined
            rounded
            :small="!$vuetify.breakpoint.mdAndDown"
            :x-small="$vuetify.breakpoint.mdAndDown"
          >
            {{ $t(`${page}.title`) }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
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
  },
  data() {
    return {
      observer: null,
      pages: [
        'imprint',
        'privacy-policy',
      ],
    };
  },
  methods: {
    goTo(name) {
      this.$router.push({ name });
    },
    handleObserver() {
      if (this.$refs.footer !== undefined) {
        const { left } = this.$refs.footer.$el.style;
        const params = { width: left.replace('px', '') };
        this.$store.dispatch('utils/setDrawer', params);
      }
    },
  },
  computed: {
    api() {
      let baseURL = 'http://localhost:8000';
      const { VUE_APP_API } = process.env;
      if (VUE_APP_API) {
        baseURL = `https://${VUE_APP_API}`;
      }
      return `${baseURL}/schema/redoc`;
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
  beforeDestroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  },
  mounted() {
    const config = {
      attributes: true,
      attributeFilter: ['style'],
    };
    const callback = () => {
      this.$nextTick(() => {
        this.handleObserver();
      });
    };
    const observer = new MutationObserver(callback);
    observer.observe(this.$refs.footer.$el, config);
    this.observer = observer;
    this.handleObserver();
  },
};
</script>

<style scoped>
.v-footer > .container {
  transition: opacity .5s ease-out;
  -moz-transition: opacity .5s ease-out;
  -webkit-transition: opacity .5s ease-out;
  -o-transition: opacity .5s ease-out;
}

.v-footer > .container.opaque {
  opacity: 0.25;
}

.v-footer .container:hover {
  opacity: 1;
}
</style>
