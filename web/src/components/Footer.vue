<template>
  <v-footer
    ref="footer"
    :dark="dark"
    padless
    fixed
    inset
    app
  >
    <v-container
      :class="{
        'px-7': $vuetify.breakpoint.mdAndDown,
        transparent: hasOpacity,
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
            small
          >
            <v-icon left>
              mdi-information-outline
            </v-icon>

            2010–{{ new Date().getFullYear() }}
          </v-btn>

          <v-chip
            v-if="!$vuetify.breakpoint.mdAndDown"
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
            small
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
            small
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
      const { left } = this.$refs.footer.$el.style;
      const params = { width: left.replace('px', '') };
      this.$store.dispatch('utils/setDrawer', params);
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
    hasOpacity() {
      const names = ['home', 'game', 'session'];
      return names.includes(this.$route.name);
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

.v-footer > .container.transparent {
  opacity: 0.25;
}

.v-footer .container:hover {
  opacity: 1;
}
</style>
